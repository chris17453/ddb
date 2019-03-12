from .language import sql_syntax
from .tokenize import tokenizer


class lexer:
   

    def __init__(self, query, debug=False):
        # select distinct,* from table where x=y and y=2 order by x,y limit 10,2
        # select c1,c2,c3,c4 as x,* from table where x=y and y=2 order by x,y limit 10,2
        # select top 10 * from table where x=y and y=2 order by x,y
        # insert into table () values ()
        # delete from table where x=y and y=2

        self.debug = debug
        self.query_objects = []
        querys = query.split(';')
        self.info("Queries", querys)
        for q in querys:
            self.info("-----------------------------------")
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
            if False == parsed:
                self.query_objects = None
                break
            self.query_objects.append(parsed)

        if None == self.query_objects:
            raise Exception("Invalid SQL")

    def parse(self, tokens):

        sql_object = []
        # SOME TODO!
        # loop through types
        debug = True
        query_object = {}
        for query in sql_syntax['query_matrix']:
            # loop through switches
            token_index = 0
            self.info("-----", query['query'])

            keyword_found = False
            switch_index = 0
            query_mode = None
            curent_object = {}
            switch = {}
            while switch_index < len(query['switch']) and token_index < len(tokens):

                self.info("Token Index", token_index, "token", tokens[token_index])
                self.info("Token Length", len(tokens))
                switch = query['switch'][switch_index]
                switch_index += 1
                curent_object = {}
                if 'dispose' in switch:
                    dispose = switch['dispose']
                else:
                    dispose = False
                if 'no_keyword' in switch:
                    no_keyword = switch['no_keyword']
                else:
                    no_keyword = False
                if 'store_array' in switch:
                    store_array = switch['store_array']
                else:
                    store_array = False

                if 'parent' in switch:
                    parent = switch['parent']
                else:
                    parent = None
                if 'type' in switch:
                    meta_type = switch['type']
                else:
                    meta_type = None

                if 'optional' in switch:
                    optional = switch['optional']
                else:
                    optional = False

                if isinstance(switch['name'], list):
                    object_id = ' '.join([str(x) for x in switch['name']])
                    object_id = object_id.lower()
                else:
                    object_id = switch['name']
                    object_id = object_id.lower()
                self.info("Object Id:", object_id, "Token Id:", token_index)
                if False == no_keyword:
                    keyword_compare = self.get_sub_array(switch, 'name')
                    haystack = self.get_sub_array_sub_key(tokens[token_index:], 'data')
                    self.info(keyword_compare)
                    if True == self.single_array_match(keyword_compare, haystack):
                        self.info("match", keyword_compare, haystack)
                        # we use name because it may be a list. and its simpler to hash by name
                        # as long as the compare is good, we dont care
                        curent_object['mode'] = object_id
                        if switch_index == 1:
                            query_mode = query['query']
                        keyword_found = True
                    else:
                        if False == optional:
                            if True == debug:
                                self.info("Exiting")
                            break
                        else:
                            continue
                    if False == keyword_found:
                        self.info("Keywords exhausted")
                        break

                    token_index += len(keyword_compare)
                    self.info("advance token index ", token_index, switch['data'])
                else:
                    curent_object['mode'] = object_id

                base_argument={}
                # set static variables
                if 'data' in  switch:
                    if 'vars' in switch['data']:
                        for var_name in switch['data']['vars']:
                            self.info("var: {0}-{1}".format(var_name,))
                            base_argument[var_name]=switch['data']['vars'][var_name]

                if None == switch['data'] or False == switch['data']:
                    self.info("No data to match")
                    # only append object after argument collection is done
                    # query_object.append(curent_object)
                    if not dispose:
                        self.info("----------Adding", curent_object['mode'])
                        query_object[curent_object['mode']] = None

                # This is where data colection happens
                else:
                    in_argument = True
                    argument_index = 0
                    while True == in_argument:

                        self.info("---in argument")

                        # DEPENDENCY
                        # DEPENDENCY
                        # DEPENDENCY

                        if 'depends_on' in switch:
                            depends_on = switch['depends_on']
                        else:
                            self.info("--- Depends on nothing")
                            depends_on = None

                        # if there is a dependency, enforce
                        if None != depends_on:

                            depends_oncompare = self.get_sub_array(depends_on)

                            dependency_found = False
                            for q_o in query_object:
                                #self.info( depends_on,q_o)
                                haystack = self.get_sub_array(q_o)
                                if True == self.single_array_match(depends_oncompare, haystack):
                                    dependency_found = True
                            if False == dependency_found:
                                self.info("Missing", depends_on)
                                break
                            else:
                                self.info("Dependency found", depends_on)

                        # self.info("data",switch['data'])
                        if 'arguments' in switch:
                            arguments = switch['arguments']
                        else:
                            arguments = 1
                        self.info("Number of arguments", arguments)

                        data = self.get_sub_array(switch, 'data')
                        match_len = 0
                        match = None
                        for sig in data:
                            signature_compare = self.get_sub_array(sig, 'sig')
                            haystack = self.get_sub_array_sub_key(tokens[token_index:], 'data')
                            if True == self.single_array_match(signature_compare, haystack):
                                #    self.info("match", signature_compare,haystack)
                                if len(signature_compare) > match_len:
                                    match_len = len(signature_compare)
                                    match = signature_compare
                                    self.info("Best Match", match_len)
                        if None == match:
                            self.info("No match")
                            break
                        else:

                            w_index = 0
                            argument = base_argument
                            for word in match:
                                variable_data=tokens[token_index + w_index]['data']
                                if word[0:1] == '[' and word[-1] == ']': 
                                    definition='array'
                                elif word[0:1] == '{' and word[-1] == '}':
                                     definition='single'
                                else:
                                    definition=None

                                # is there an definition?
                                if definition:
                                    # if we have definitions
                                    variable=word[1:-1]
                                    variable_type='string'
                                    if 'specs' in switch:
                                        # if this is in or definitions
                                        if variable in switch['specs']:
                                            if 'type' in switch['specs'][variable]:
                                                variable_type=switch['specs'][variable]['type']
                                            
                                    if variable_type=='int':
                                        try:
                                            argument[variable] = tokens[token_index + w_index]['data'] = int(variable_data)
                                        except BaseException:
                                            raise Exception ("Variable data not an integer")
                                    elif variable_type=='bool':
                                        if variable_data.lower()=='true':
                                            argument[variable] =True
                                        elif variable_data.lower()=='false':
                                            argument[variable] =False
                                        else:
                                            raise Exception("Variable Data not boolean")
                                    elif variable_type=='char':
                                        if len(variable_data)!=1:
                                            raise Exception("variable data length exceeded, type char")
                                        argument[variable] =variable_data

                                    elif variable_type=='string':
                                        argument[variable] =variable_data
                                else:
                                    # normal keyword
                                    argument[word] = variable_data
                                w_index += 1
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
                                    if True == store_array:
                                        if curent_object['mode'] not in query_object:
                                            query_object[curent_object['mode']] = []

                                        query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                    else:
                                        if None == parent:
                                            if meta_type=='single':
                                                for arg_key in curent_object['arguments']:
                                                    query_object[arg_key] = curent_object['arguments'][arg_key]
                                            else:    
                                                query_object[curent_object['mode']] = curent_object['arguments']
                                            self.info("NO APPEND")
                                        else:
                                            self.info("APPEND")
                                            query_object[parent].append({curent_object['mode']: curent_object['arguments']})
                                    jump = None
                                    if 'jump' in switch:
                                        self.info("JUMP")
                                        jump = switch['jump']
                                    if None != jump:
                                        tsi = 0
                                        for ts in query['switch']:
                                            if ts['name'] == jump:
                                                self.info("Jumping from ", switch_index, tsi + 1)
                                                switch_index = tsi + 1
                                                break
                                            tsi += 1
                                    in_argument = False

                                    in_argument = False
                            else:
                                self.info("in list")

                                if len(tokens) <= token_index:
                                    self.info("at the end")
                                    if True == store_array:
                                        if curent_object['mode'] not in query_object:
                                            query_object[curent_object['mode']] = []

                                        query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                    else:
                                        if None == parent:
                                            #print curent_object
                                            query_object[curent_object['mode']] = curent_object['arguments']
                                            self.info("NO APPEND")

                                        else:
                                            self.info("APPEND")
                                            query_object[parent].append({curent_object['mode']: curent_object['arguments']})

                                # look ahead to see if its a list ","
                                if len(tokens) > token_index:
                                    self.info("--looking ahead")
                                    # if its not exit
                                    self.info("----", tokens[token_index]['data'])
                                    if tokens[token_index]['data'] != ',':
                                        self.info("---not list")
                                        # only append object after argument collection is done
                                        self.info("----------Adding", curent_object['mode'])
                                        if True == store_array:
                                            if curent_object['mode'] not in query_object:
                                                query_object[curent_object['mode']] = []

                                            query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                        else:
                                            if None == parent:
                                                #print curent_object
                                                query_object[curent_object['mode']] = curent_object['arguments']
                                                self.info("NO APPEND")

                                            else:
                                                self.info("APPEND")
                                                query_object[parent].append({curent_object['mode']: curent_object['arguments']})
                                        jump = None
                                        if 'jump' in switch:
                                            jump = switch['jump']
                                        if None != jump:
                                            tsi = 0
                                            for ts in query['switch']:
                                                if ts['name'] == jump:
                                                    self.info("Jumping from ", switch_index, tsi + 1)
                                                    switch_index = tsi + 1
                                                    break
                                                tsi += 1
                                        in_argument = False
                                    else:
                                        self.info("------more list")
                                        token_index += 1

            # This is where we exit if we reached the end of processing with a full length
            #print token_index,len(tokens)
            self.info(switch_index, token_index, len(tokens))


            self.info(curent_object)
            if token_index == len(tokens):
                result=self.validate(curent_object,tokens,token_index,switch,query,switch_index,query_object,query_mode)
                if False == result:
                    break
                else:
                    return result

        
        
        # if
        return False





    # this is crappy, I'm just breaking up a giant function. Will clean later...
    def validate(self,curent_object,tokens,token_index,switch,query,switch_index,query_object,query_mode):
        self.info(curent_object)
        # so we have run out of text to match and everything is good so far
        self.info("############################think its a match")

        if 'arguments' not in curent_object and 'arguments' in switch:
            self.info("Missing argument in last element")
            bad = True
            return False

        # lets make sure the rest are optional
        if len(query['switch']) >= switch_index:
            self.info("still checking")
            bad = False
            for t in range(switch_index, len(query['switch'])):
                if 'optional' not in query['switch'][t]:
                    bad = True
                    return False

                else:
                    if not query['switch'][t]['optional']:
                        bad = True
                        return False

            if True == bad:
                self.info("Not successful. required arguments missing")
                return False

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
                        for f in sql_syntax['functions']:
                            if f['name'] == node['function']:
                                argindex = 1
                                if f['arguments'] is not None:
                                    for arg in f['arguments']:
                                        if arg['required']:
                                            # if this argument key is not in the node dict
                                            if 'argument{0}'.format(argindex) not in node:
                                                self.info("Missing arguments")
                                                return False
                                        argindex += 1

                                else:
                                    argindex = 0
                                if 'argument{0}'.format(argindex + 1) in node:
                                    self.info("Too many arguments")
                                    return False

                            valid_function_name = True
                            break
                    if False == valid_function_name and True == is_function:
                        self.info("FAIL", "This isnt a valid function", node['function'])
                        return False
            else:
                self.info("No columns in select")
                return False

        self.info("SUCCESS")
        #from pprint import pprint
        #pprint( sql_object)
        sql_object = {'mode': query_mode, 'meta': query_object}
        return sql_object

    # expand columns
    # TODO null trapping
    def expand_columns(self, query_object, columns):
        if 'columns' in query_object['meta']:
            expanded_select = []
            for item in query_object['meta']['columns']:
                if 'column' in item:
                    if item['column'] == '*':
                        for column in columns:
                            expanded_select.append({'column': column})
                    else:
                        expanded_select.append(item)
                if 'function' in item:
                    expanded_select.append(item)

            query_object['meta']['columns'] = expanded_select
        # ?? needed

    # support funcitons

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

    # for tokens ['data']

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
            # ran out of haystack to test. not a match
            if index >= len(temp_haystacks):
                return False
            haystack = temp_haystacks[index]
            # not a match
            if needle[0:1] != '{' and needle[-1] != '}':
                if needle.lower() != haystack.lower():
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

