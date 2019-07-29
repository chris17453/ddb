# cython: linetrace=True

from .language import language
from .tokenize import tokenizer


class lexer:
   
    __slots__=['keep_non_keywords','debug','query_objects']

    def split(self,data,delimiter=';'):
        in_block    = None
        curent_block= None
        last_index  = 0
        index       = 0
        blocks      = [ ['\'', '\'', 'quote'], # string block
                        ['"' , '"' , 'quote'], # string block
                        ['[' , ']' , 'db'   ], # mssql column
                        ['`' , '`' , 'db'   ], # mysql column
                    ]
        
        list_of_strings=[]                     # the list of split strings

        for c in data:
            if not in_block:
                for block in blocks:
                    if c==block[0]:
                        in_block=True
                        curent_block=block
                        break

            else:
                if c==curent_block[1]:
                    in_block=None
                    curent_block=None
                index+=1
                continue

            if c==delimiter:
                list_of_strings.append(data[last_index:index])
                last_index=index+1
            index+=1
        if index!=last_index:
                list_of_strings.append(data[last_index:])
        return list_of_strings


    def __init__(self, query, debug=None):
        #queries=self.split(query,';')
        #print "****"
        #for q in queries:
        #    print q
        #print "****"

        # select distinct,* from table where x=y and y=2 order by x,y limit 10,2
        # select c1,c2,c3,c4 as x,* from table where x=y and y=2 order by x,y limit 10,2
        # select top 10 * from table where x=y and y=2 order by x,y
        # insert into table () values ()
        # delete from table where x=y and y=2

        # keep non variable keywords form signature match in object
        # realy only need this for debugging
        self.keep_non_keywords=True
        self.debug = debug
        self.query_objects = []
        if  query==None:
            raise Exception("Invalid Syntax")
    
        #print query
        
        print("---------------------")
        querys = self.split(query,';')
        print querys
        querys = query.split(';')
        self.info("Queries", querys)
        print querys
        for q in querys:
            self.info("-----------------------------------")
            if q and q.isspace():
                continue
            tokens = tokenizer().chomp(q, discard_whitespace=True, debug=debug)
            # skip 0 length commands such as single ';'
            token_length = 0
            for token in tokens:
                if token['data'] != '':
                    token_length += 1

            self.info("Token Length", token_length)
            if token_length == 0:
                continue

            parsed = self.parse(tokens)
            if None == parsed['success']:
                raise Exception(parsed['msg'])
            else:
                if None == parsed['results']:
                    continue
                self.query_objects.append(parsed['results'])

        if len(self.query_objects)==0:
            raise Exception("Invalid Syntax")

    def get_argument(self,word,segment,tokens,token_index,w_index):
       # if we have definitions
        variable_data=tokens[token_index + w_index]['data']
        first_char=word[0:1]
        last_char=word[-1]
        #if first_char == '[' and last_char == ']': 
        #    definition='array'
        if first_char == '{' and last_char == '}':
                definition='single'
        elif first_char == '$':
            definition='internal'
        else:
            definition=None       

        # HERE ADD add string length enforcment for colon +1 -1 same for brackets
        
        if definition=='single':
            variable=word[1:-1]
            variable_type='string'
            if 'specs' in segment:
                # if this is in or definitions
                if variable in segment['specs']:
                    if 'type' in segment['specs'][variable]:
                        variable_type=segment['specs'][variable]['type']
                    
            argument=None
            if variable_type=='int':
                try:
                    tokens[token_index + w_index]['data'] = int(variable_data)
                    argument = tokens[token_index + w_index]['data'] 
                except BaseException:
                    err_msg="Variable data not an integer '{0}'".format(variable_data,)
                    raise Exception (err_msg)
            elif variable_type=='bool':
                if variable_data.lower()=='true':
                    argument=True
                elif variable_data.lower()=='false':
                    argument =False
                else:
                    raise Exception("Variable Data not boolean")
            elif variable_type=='char':
                if len(variable_data)!=1:
                    raise Exception("variable data length exceeded, type char")
                argument =variable_data
            #default catch
            elif variable_type=='string':
                argument =variable_data
            
            return {'key':variable,'value':argument}
        elif definition=='internal':
            # here we map the possible approved calue to the keywrd or alternate, pre approved in matching function at end of file
            variable=word[1:]
            index_of_colon=variable.find(':')
            if index_of_colon!=-1:
                #variable=word[0:index_of_colon-1]
                key=variable[index_of_colon+1:].lower()
            else:
                key=variable.lower()
            return {'key':key,'value':variable_data}
            
        else:
           # normal keyword
           if self.keep_non_keywords:
               return {'key':word,'value':variable_data}
        
        raise Exception ("Not found argument")
        

    def parse(self, tokens):
        # SOME TODO!
        # loop through commands, return the first matching result
        # return the exact match, OR the match with the highest score
        highest_match=-1
        recent_match=None
        for command in language['commands']:
            res=self.test_syntax(command,tokens)
            if res['success']:
                #print (res)
                return res
            else:
                if res['match']>highest_match:
                    highest_match=res['match']
                    recent_match=res

        return recent_match
    # place holder for the status of a command fragment
    class flags:
        __slots__=['dispose','no_keyword','store_array','parent','meta_type','optional','object_id','arg_key']


        def __init__(self,command_fragment):
            if 'dispose' in command_fragment:
                self.dispose = command_fragment['dispose']
            else:
                self.dispose = False
            if 'no_keyword' in command_fragment:
                self.no_keyword = command_fragment['no_keyword']
            else:
                self.no_keyword = False
            if 'store_array' in command_fragment:
                self.store_array = command_fragment['store_array']
            else:
                self.store_array = False
            if 'key' in command_fragment:
                self.arg_key=command_fragment['key']
            else: 
                self.arg_key=None
            if 'parent' in command_fragment:
                self.parent = command_fragment['parent']
            else:
                self.parent = None
            if 'type' in command_fragment:
                self.meta_type = command_fragment['type']
            else:
                self.meta_type = None
            if 'optional' in command_fragment:
                self.optional = command_fragment['optional']
            else:
                self.optional = False
            if isinstance(command_fragment['name'], list):
                self.object_id = ' '.join([str(x) for x in command_fragment['name']])
                self.object_id = self.object_id.lower()
            else:
                self.object_id = command_fragment['name'].lower()
            #logic
            # key override for segment
            if self.arg_key:
                self.object_id=self.arg_key

                
    def test_syntax(self,command,tokens):
        query_object = {}
        token_index = 0
        self.info("-----", command['name'])
        segment_index = 0
        query_mode = None
        curent_object = {}
        segment = {}
        token_list=[]
        for i in range(0,len(tokens)):
            token_list.append("{0}-{1}".format(i,tokens[i]['data']))
        self.info(",".join(token_list))

        while segment_index < len(command['segments']) and token_index < len(tokens):
            # set the state
            segment = command['segments'][segment_index]
            self.info("############# TESTING : {0}.{1}".format(command['name'],segment['name']))
            segment_index += 1
            curent_object = {}
            base_argument={}
            in_argument = True
            argument_index = 0

            flags=lexer.flags(segment)
    
            curent_object['mode'] = flags.object_id
            query_mode = command['name']
            self.info("Object Id:", flags.object_id, "Token Id:", token_index)

            while True == in_argument:
                if 'depends_on' in segment:
                    depends_on = segment['depends_on']
                    if len(depends_on)>0:
                        if depends_on[0]=='.':
                            depends_on=depends_on[1:]
                
                    self.info("Depends on key: '{0}'".format(depends_on))
                else:
                    depends_on = None

                # if there is a dependency, enforce
                if depends_on:
                    self.info ("QUERY OBJECT:", query_object)
                    dependency_found=None
                    if depends_on in query_object:
                            dependency_found=True

                    if dependency_found:
                        self.info("Dependency found", depends_on)
                    else:
                        self.info("Missing", depends_on)
                        break

                # self.info("data",segment['data'])
                if 'arguments' in segment:
                    arguments = segment['arguments']
                else:
                    arguments = 1
                if arguments == None:
                    arguments = 1
                self.info("Number of arguments", arguments)

                
                match_len = 0
                match = None
                for partial in segment['data']:
                    signature_compare = partial['signature']
                    haystack = self.get_sub_array_sub_key(tokens[token_index:], 'data')
                    if True == self.single_array_match(signature_compare, haystack):
                        #    self.info("match", signature_compare,haystack)
                        if len(signature_compare) > match_len:
                            match_len = len(signature_compare)
                            match = signature_compare
                            signature=partial
                            self.info("Best Match", match_len)
                if None == match:
                    self.info("No match")
                    break
                else:
                    # add the static vars
                    base_argument={}
                    if 'vars' in signature:
                        for var_name in signature['vars']:
                            self.info("var","'{0}'='{1}'".format(var_name,signature['vars'][var_name]))
                            base_argument[var_name]=signature['vars'][var_name]

                    argument = base_argument
                    for w_index in range(0,len(match)):
                        word=match[w_index]
                        try:
                            computed=self.get_argument(word,segment,tokens,token_index,w_index)
                            argument[computed['key']]=computed['value']
                        except Exception as ex:
                            break
                            
                        
                        

                    if 'arguments' not in curent_object:
                        curent_object['arguments'] = []

                    if arguments == 1:
                        curent_object['arguments'] = argument
                    else:
                        # add the arguments to curent object
                        curent_object['arguments'].append(argument)

                    self.info("match", match)
                    token_index += len(match)
                    if arguments != 0:
                        self.info("print not in list")
                        argument_index += 1
                        if argument_index >= arguments:
                            self.info("----------Adding", curent_object['mode'])
                            if True == flags.store_array:
                                if curent_object['mode'] not in query_object:
                                    query_object[curent_object['mode']] = []

                                query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                            else:
                                if None == flags.parent:
                                    if flags.meta_type=='single':
                                        for flags.arg_key in curent_object['arguments']:
                                            query_object[flags.arg_key] = curent_object['arguments'][flags.arg_key]
                                    else:    
                                        query_object[curent_object['mode']] = curent_object['arguments']
                                    self.info("NO APPEND")
                                else:
                                    self.info("APPEND")
                                    if flags.parent not in query_object:
                                        query_object[flags.parent]=[]
                                    query_object[flags.parent].append({curent_object['mode']: curent_object['arguments']})
                            jump = None
                            if 'jump' in segment:
                                self.info("JUMP")
                                jump = segment['jump']
                            if None != jump:
                                tsi = 0
                                for ts in command['segments']:
                                    if ts['name'] == jump:
                                        self.info("Jumping from ", segment_index, tsi + 1)
                                        segment_index = tsi + 1
                                        break
                                    tsi += 1
                            in_argument = False
                    else:
                        self.info("in list")

                        if len(tokens) <= token_index:
                            self.info("at the end")
                            if True == flags.store_array:
                                if curent_object['mode'] not in query_object:
                                    query_object[curent_object['mode']] = []

                                query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                            else:
                                if None == flags.parent:
                                    #print curent_object
                                    query_object[curent_object['mode']] = curent_object['arguments']
                                    self.info("NO APPEND")

                                else:
                                    self.info("APPEND")
                                    if flags.parent not in query_object:
                                        query_object[flags.parent]=[]
                                    query_object[flags.parent].append({curent_object['mode']: curent_object['arguments']})

                        # look ahead to see if its a list ","
                        if len(tokens) > token_index:
                            self.info("--looking ahead")
                            # if its not exit
                            self.info("----", tokens[token_index]['data'])
                            if tokens[token_index]['data'] != ',':
                                self.info("---not list")
                                # only append object after argument collection is done
                                self.info("----------Adding", curent_object['mode'])
                                if True == flags.store_array:
                                    if curent_object['mode'] not in query_object:
                                        query_object[curent_object['mode']] = []

                                    query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                else:
                                    if None == flags.parent:
                                        #print curent_object
                                        query_object[curent_object['mode']] = curent_object['arguments']
                                        self.info("NO APPEND")

                                    else:
                                        self.info("APPEND")
                                        if flags.parent not in query_object:
                                            query_object[flags.parent]=[]
                                        query_object[flags.parent].append({curent_object['mode']: curent_object['arguments']})
                                jump = None
                                if 'jump' in segment:
                                    jump = segment['jump']
                                if None != jump:
                                    tsi = 0
                                    for ts in command['segments']:
                                        if ts['name'] == jump:
                                            self.info("Jumping from ", segment_index, tsi + 1)
                                            segment_index = tsi + 1
                                            break
                                        tsi += 1
                                in_argument = False
                            else:
                                self.info("------more list")
                                token_index += 1

        # This is where we exit if we reached the end of processing with a full length
        #print token_index,len(tokens)
        self.info(segment_index, token_index, len(tokens))


        self.info(query_object)
        if token_index == len(tokens):

            result=self.validate(curent_object,tokens,token_index,segment,command,segment_index,query_object,query_mode)
            if  result['success']:
                self.info("SUCCESSFULL MATCH")
                return {'success':True,'results':result,'match':token_index,'msg':None}
            else:
                self.info("FAILED MATCH")
                return {'success':None,'results':None,'match':token_index,'msg':result['msg']}

        query_err=[]
        for index in range(0,len(tokens)):
            if index==token_index:
                query_err.append(" >>> ")    
                query_err.append(tokens[index]['data'])
                query_err.append(" <<< ")    
            else:
                query_err.append(tokens[index]['data'])
        query_err.append("\n Syntax error near word {0}".format(token_index))
        err_msg=" ".join(query_err)
        self.info("FAILED MATCH")
        return {'success':None,'results':None,'match':token_index,'msg':err_msg}





    # this is crappy, I'm just breaking up a giant function. Will clean later...
    def validate(self,curent_object,tokens,token_index,segment,command,segment_index,query_object,query_mode):
        self.info(curent_object)
        # so we have run out of text to match and everything is good so far
        self.info("############################think its a match")

        if 'arguments' not in curent_object and 'arguments' in segment:
            self.info("Missing argument in last element")
            bad = True
            return False

        # lets make sure the rest are optional
        if len(command['segments']) >= segment_index:
            self.info("still checking")
            bad = False
            for t in range(segment_index, len(command['segments'])):
                if 'optional' not in command['segments'][t]:
                    bad = True
                    msg="Non optional components missing from query"
                    return {'success':None,'msg':msg}
                else:
                    if not command['segments'][t]['optional']:
                        bad = True
                        msg="Non optional components missing from query"
                        return {'success':None,'msg':msg}


            if True == bad:
                msg="Not successful. required arguments missing"
                self.info(msg)
                return {'success':None,'msg':msg}

        self.info("Query object", query_object)
        if query_mode == 'select':
            # check to make sure functions are valid
            self.info("Validating Select Functions")
            if 'columns' in query_object:
                for node in query_object['columns']:
                    valid_function_name = False
                    is_function = False
                    if 'function' in node:
                        is_function = True
                        self.info("It's a function!")
                        for f in language['functions']:
                            if f['name'] == node['function']:
                                argindex = 1
                                if f['arguments'] is not None:
                                    for arg in f['arguments']:
                                        if arg['required']:
                                            # if this argument key is not in the node dict
                                            if 'argument{0}'.format(argindex) not in node:
                                                msg="Missing arguments"
                                                self.info(msg)
                                                return {'success':None,'msg':msg}

                                        argindex += 1

                                else:
                                    argindex = 0
                                if 'argument{0}'.format(argindex + 1) in node:
                                    msg="Too many arguments"
                                    self.info(msg)
                                    return {'success':None,'msg':msg}

                            valid_function_name = True
                            break
                    if False == valid_function_name and True == is_function:
                        msg="'{0}' isn't a valid function".format(node['function'])
                        self.info(msg)
                        return {'success':None,'msg':msg}
            else:
                msg="No columns in select"
                self.info(msg)
                return {'success':None,'msg':msg}

        self.info("SUCCESS")
        #from pprint import pprint
        #pprint( sql_object)
        sql_object = {'success':True,'mode': query_mode, 'meta': query_object}
        return sql_object

    # expand columns...TODO: REMOVE AFTER MIGRATION 
    # TODO null trapping
    #def expand_columns(self, meta, columns):
    #    if meta.columns:
    #        expanded_select = []
    #        for item in meta.columns:
    #            if item.column:
    #                if item.column == '*':
    #                    for column in columns:
    #                        expanded_select.append({'column': column})
    #                else:
    #                    expanded_select.append(item)
    #            if 'function' in item:
    #                expanded_select.append(item)
#
    #        meta.columns = expanded_select
    #    # ?? needed
#
    ## support funcitons

    def get_sub_array(self, array, key=None):
        if None == key:
            if isinstance(array, str):
                return [array]
            else:
                return array
        if True == isinstance(array[key], list):
            return array[key]
        else:
            return [array[key]]


    def get_sub_array_sub_key(self, array, key):
        temp_array = []

        for item in array:
            temp_array.append(item[key])

        return temp_array

    def single_array_match(self, needles, haystacks):
        """ Match a single or array of strings with with another string or array of strings"""

        # make needels an array, with or without a sub key
        if isinstance(needles, str):
            temp_needles = [needles]
        else:
            temp_needles = needles

        # make haystacks an array
        if isinstance(haystacks, str):
            temp_haystacks = [haystacks]
        else:
            temp_haystacks = haystacks

        # now we have 2 plain array/lists to compare

        index = 0

        for needle in temp_needles:
            first_char=needle[0]
            last_char=needle[-1]
            
            # ran out of haystack to test. not a match
            if index >= len(temp_haystacks):
                return False
            haystack = temp_haystacks[index]
            # not a match
            if first_char!='$':
                if first_char != '{' and last_char != '}':
                    if needle.lower() != haystack.lower():
                        return False
            if needle[0]=='$':
                variable=needle[1:]
                index_of_colon=variable.find(':')
                if index_of_colon!=-1:
                    variable=variable[0:index_of_colon]

            #    print(needle,haystack)
            #    print(variable)
                if variable in language:
                    if haystack not in language[variable]:
                        return False

            index += 1
        # if we got here it must match
        return True

    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug:
            if arg3 is None and arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return
            if arg3 is None:
                print("{0} {1} {2}".format(msg, arg1, arg2))
                return
            if arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return

            print("[{0}]".format(msg))

