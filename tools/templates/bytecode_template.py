import timeit

### ----                                     ----
### ddb BYTECODE LANGUAGE DEFINITIONS
### ----                                     ----
### Automagically generated, dont mess with this.
### ----  or you will be eaten by unicorns   ----
### ----                                     ----

# each word is given an integer value based on section, sections increment based on SECTION BLOCK_VALUE

# R=Reserved word
# K=Key word
# B=Block    such as comment, text or code
# O=Operator
# D=Delimiter
# A=Alpha
# N=Numeric
# comparisons are ordered to be done in greatest length order, to prevent uneven length but similar values
# this also doubles as a speed enhancement



class bytecode:
    TOKEN_TYPE_FIELD        = 10
    TOKEN_TYPE_BLOCK_STRING = 20
    TOKEN_TYPE_STRING       = 30
    TOKEN_TYPE_COMMENT      = 40
    TOKEN_TYPE_WHITESPACE   = 50
    TOKEN_TYPE_EXPRESSION   = 60
    TOKEN_TYPE_OTHER        = 70
    TOKEN_TYPE_KEYWORD      = 80
    TOKEN_TYPE_RESERVED     = 90
    TOKEN_TYPE_NUMERIC      = 100
    TOKEN_TYPE_OPERATOR     = 110
    TOKEN_TYPE_DELIMITER    = 120
    TOKEN_TYPE_FUNCTION     = 130

    ERROR_RESERVERD_WORD_REQUIRES_IDENTIFYER = 10
    ERROR_INVALID_IDENTIFYER_TYPE            = 20

    IGNORE_WHITESPACE       =True
    IGNORE_COMMENTS         =True

{section_range}

{vars}

    @staticmethod
    def get_intermediate_code_2(text):
        if text==None: return 0
        text=text.upper()
        text_length=len(text)
        text_hash=hash(text)
        if   text=='': 
            return 0 
{get_intermediate_code_2}
        return 0


    @staticmethod
    def get_intermediate_code_3(text):
        if text==None: return 0
        text=text.upper()
        text_length=len(text)
        text_hash=hash(text)
        if   text=='': 
            return 0 
{get_intermediate_code_3}
        return 0



    @staticmethod
    def get_code_type(code):
        if code>=bytecode.BLOCK_START     and code<=bytecode.BLOCK_END:      return bytecode.TOKEN_TYPE_BLOCK_STRING
        if code>=bytecode.RESERVED_START  and code<=bytecode.RESERVED_END:   return bytecode.TOKEN_TYPE_RESERVED
        if code>=bytecode.KEYWORD_START   and code<=bytecode.KEYWORD_END:    return bytecode.TOKEN_TYPE_KEYWORD
        if code>=bytecode.OPERATOR_START  and code<=bytecode.OPERATOR_END:   return bytecode.TOKEN_TYPE_OPERATOR
        if code>=bytecode.NUMERIC_START   and code<=bytecode.NUMERIC_END:    return bytecode.TOKEN_TYPE_NUMERIC
        if code>=bytecode.ALPHA_START     and code<=bytecode.ALPHA_END:      return bytecode.TOKEN_TYPE_STRING
        if code>=bytecode.DELIMITER_START and code<=bytecode.DELIMITER_END:  return bytecode.TOKEN_TYPE_DELIMITER
        if code>=bytecode.FUNCTION_START  and code<=bytecode.FUNCTION_END:  return bytecode.TOKEN_TYPE_FUNCTION
        #print code
        #print  bytecode.ALPHA_START , bytecode.ALPHA_END, bytecode.TOKEN_TYPE_ALPHA
        return 0

    @staticmethod
    def add_fragment(fragment='',fragment_length=0,uid='',fragment_id=0,fragment_type=None,depth=0):
        #print ".",fragment 
        new_fragments=[]
        error=0
        # ignore whitespace if configured
        if fragment_type==bytecode.TOKEN_TYPE_WHITESPACE and bytecode.IGNORE_WHITESPACE:
            return new_fragments
        elif fragment_type==bytecode.TOKEN_TYPE_COMMENT and bytecode.IGNORE_COMMENTS:
             return new_fragments

        # add all identfyer blocks... must only contain reserved words or db target.. , 
        # words after a "." do not require identifier brackets....
        elif fragment_type==bytecode.TOKEN_TYPE_FIELD:
            code=bytecode.get_intermediate_code_2(fragment)
            computed_fragment_type=fragment_type
            if code!=0:
                computed_fragment_type=bytecode.get_code_type(code)
                if computed_fragment_type!=bytecode.TOKEN_TYPE_RESERVED:
                    error=bytecode.ERROR_INVALID_IDENTIFYER_TYPE


            new_fragments.append([fragment,code,depth,uid,fragment_id,computed_fragment_type,error])
            return new_fragments
            
        elif fragment_type==bytecode.TOKEN_TYPE_BLOCK_STRING or fragment_type==bytecode.TOKEN_TYPE_COMMENT or fragment_type==bytecode.TOKEN_TYPE_WHITESPACE:
            #print fragment,fragment_type
            if fragment!="":
                new_fragments.append([fragment,0,depth,uid,fragment_id,fragment_type,error])
                return new_fragments
        
        # Add all strings, test for system or reserved
        elif  fragment_type==bytecode.TOKEN_TYPE_STRING:
            code=bytecode.get_intermediate_code_2(fragment)
            
            if code!=0:
                computed_fragment_type=bytecode.get_code_type(code)
            else:
                computed_fragment_type=fragment_type

            #if computed_fragment_type==bytecode.TOKEN_TYPE_RESERVED:
            #    error=bytecode.ERROR_RESERVERD_WORD_REQUIRES_IDENTIFYER
            new_fragments.append([fragment,code,depth,uid,fragment_id,computed_fragment_type,error])
            return new_fragments

        # its a bunch of delimiters, break it up and match if possible
        else:
            if fragment!="":
                right_fragment=""
                right_fragment_length=0


                while fragment_length>0:
                    found=None
                    for length in xrange(fragment_length,0,-1):
                        code=bytecode.get_intermediate_code_2(fragment[:length])
                        if code!=0:
                            if right_fragment_length>0:
                                computed_fragment_type=code#bytecode.get_code_type(code)
                                new_fragments.append([right_fragment,0,depth,uid,fragment_id,computed_fragment_type,error])
                                right_fragment_length=0
                                right_fragment=""

                            found=True
                            computed_fragment_type=bytecode.get_code_type(code)
                            new_fragments.append([fragment[:length],code,depth,uid,fragment_id,computed_fragment_type,error])
                            fragment_length-=length
                            if fragment_length>0:
                                fragment=fragment[length:]
                            break;
                    
                    # if we looped through all length combiniations and found nothing, add the remainder and shrink the stack
                    if found==None:
                        right_fragment+=fragment[0]
                        right_fragment_length+=1
                        fragment_length-=1
                        if fragment_length>0:
                            fragment=fragment[1:]
                # catch all
                if right_fragment_length>0:

                    new_fragments.append([right_fragment,0,depth,uid,fragment_id,fragment_type,error])
                    right_fragment_length=0


        return new_fragments
   
    @staticmethod
    def get_BYTECODE(data,depth=0,uid="1",fragment_id=1):
        fragments=[]
        fragment=""
        fragment_length=0
        fragment_type=None
        in_block=None
        in_alpha=None
        block_depth=0
        # main loop for tokenizing
        for c in data:
            
            if in_block:
                in_alpha=None

                # is it the other side of the block
                if c==bytecode.LEFT_PAREN_STR and in_block==bytecode.RIGHT_PAREN_STR:      
                    block_depth+=1
                    fragment+=c
                    fragment_length+=1
                    continue

                
                temp_test=fragment+c
                in_block_len=len(in_block)
                test_index_length=len(temp_test)
                test_index=test_index_length-in_block_len
                temp_test[test_index:]
                
                
                
                #print '>'+temp_test[test_index:]+'<' 
                #print '>'+in_block+'<' 
                #print '>'+fragment[test_index:]+'.'+in_block
                if test_index_length>=in_block_len and temp_test[test_index:]==in_block:
                         
                    if in_block==bytecode.RIGHT_PAREN_STR:
                        #print 'HI'+fragment+str(block_depth)

                        block_depth-=1
                        if block_depth!=0:
                            fragment+=c
                            fragment_length+=1
                            continue


                        # last character hasnt been added, but maybe others have. pull off the stack
                        #if in_block_len>0:
                        #    #print len(in_block),fragment+"-EDGE"
                        #1    fragment=fragment[0:-1]
                        #print fragment +'---'
                           
                        sub_code=bytecode.get_BYTECODE(fragment,depth+1,"{0}.{1}".format(uid,fragment_id),fragment_id)
                        #fragment_id=sub_code[1]['fragment_id']+1
                        fragment_id=sub_code[1]
                        fragments+=sub_code[0]
                    else:
                        # last character hasnt been added, but maybe others have. pull off the stack
                        if in_block_len>1:
                            #print len(in_block),fragment+"-EDGE"
                            fragment=fragment[:-in_block_len+0]

                        fragment_id+=1
                        fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                        fragment_type=None
                    fragment=""
                    fragment_length=0
                    in_block=None
                # no, add the contents
                else:
                    fragment+=c
                    fragment_length+=1
            else:
                # self closing or single character match
                if   c==bytecode.DOUBLE_QUOTE_STR:    
                    in_block  =bytecode.DOUBLE_QUOTE_STR
                    frag_temp =bytecode.TOKEN_TYPE_BLOCK_STRING
                elif c==bytecode.SINGLE_QUOTE_STR:    
                    in_block  =bytecode.SINGLE_QUOTE_STR
                    frag_temp =bytecode.TOKEN_TYPE_BLOCK_STRING
                elif c==bytecode.BACK_TIC_STR:        
                    in_block  =bytecode.BACK_TIC_STR
                    frag_temp =bytecode.TOKEN_TYPE_FIELD
                elif c==bytecode.LEFT_PAREN_STR:      
                    in_block  =bytecode.RIGHT_PAREN_STR
                    frag_temp =bytecode.TOKEN_TYPE_EXPRESSION
                    block_depth   +=1
        
                # matched pair, multi character
                test_fragment=fragment+c
                if test_fragment==bytecode.LEFT_COMMENT_STR:    
                    in_block  =bytecode.RIGHT_COMMENT_STR
                    frag_temp =bytecode.TOKEN_TYPE_COMMENT
                    fragment=""
                    fragment_length=0
                    
                elif test_fragment==bytecode.COMMENT_SINGLE_STR:  
                    fragment=""
                    fragment_length=0
                    in_block  =bytecode.NEW_LINE_STR
                    frag_temp =bytecode.TOKEN_TYPE_COMMENT

                
                if c==bytecode.SPACE_STR or c==bytecode.TAB_STR or c==bytecode.NEW_LINE_STR:
                    fragment_id+=1
                    fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                    fragments+=bytecode.add_fragment(c,fragment_length,uid,fragment_id,depth=depth,fragment_type=bytecode.TOKEN_TYPE_WHITESPACE)
                    fragment_type=None
                    fragment=""
                    fragment_length=0
                    continue
                    
                if in_block:
                    fragment_id+=1
                    fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                    fragment_type=frag_temp
                    fragment=""
                    fragment_length=0
                    continue
                    
                #not a block, or anything else
                #if 1==1:
                else:
                    # is this the start of an "WORD"
                    u_alpha   =c>=bytecode.A_STR and c<=bytecode.Z_STR
                    l_alpha   =c>=bytecode.a_STR and c<=bytecode.z_STR 
                    numeric   =c>=bytecode.ZERO_STR and c<=bytecode.NINE_STR
                    underscore=c==bytecode.UNDERSCORE_STR 
                    dollar    =c==bytecode.DOLLAR_STR

                    if fragment_type!=bytecode.TOKEN_TYPE_STRING:
                        if u_alpha or l_alpha or numeric or underscore or dollar:
                            fragment_id+=1
                            fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                            fragment=c
                            fragment_length=1
                            fragment_type=bytecode.TOKEN_TYPE_STRING
                            continue    
    
                    
                    # Are we in a "WORD"
                    else:
                        # If we just LEFT ... add the existing word, and start a new one
                        if not u_alpha and not l_alpha and not numeric and not underscore and not dollar:
                            fragment_id+=1
                            fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                            fragment=c
                            fragment_length=1
                            fragment_type=bytecode.TOKEN_TYPE_OTHER
                            continue

                        
                    # fallthrough
                    fragment+=c
                    fragment_length+=1

        # END Loop                
        # if anything is still left in the pipeline, cleanup
        
        fragment_id+=1
        fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
        fragment=""
        fragment_length=0
    
    
        # err if block mismatch
        #if in_block:
        #    err_msg="Missing {0}".format(in_block)
        #    raise Exception(err_msg)
        
        # reduce groups that are single elements
        #while len(fragments)==1:
        #    print fragments
        #    elif isinstance(fragments,dict):
        #        fragments=fragments['sub']
        #    print fragments
        #    return fragments
        
        #return [{"sub":fragments,'fragment_id':fragment_id}]
        return [fragments,fragment_id]

    

    @staticmethod
    def print_code(codes,root=True):
        if root: print("Token                | Code   | Depth | UID         | Fragment ID | Type                 | Error  | Level")
        if root: print("---------------------+--------+-------+-------------+-------------+----------------------+--------+------ ")
        if isinstance(codes,list):
            for code in codes:
                #if isinstance(code,dict):
                #    bytecode.print_code(code['sub'],None)
                #elif isinstance(code,list):
                    pad=""
                    for i in range(code[2]):
                        pad+=" " 
                    level=pad+code[0]
                    if len(level)>15:
                        level=level[:15]+'...'
                    level=level.replace('\n',' ')
                    word=code[0]
                    if len(word)>15:
                        word=level[:15]+'...'
                    word=word.replace('\n',' ')
                    fragment_type=code[5]
                    error=code[6]
                    if   code[5]==bytecode.TOKEN_TYPE_FIELD       : fragment_type="FIELD"
                    elif code[5]==bytecode.TOKEN_TYPE_BLOCK_STRING: fragment_type="BLOCK_STRING"
                    elif code[5]==bytecode.TOKEN_TYPE_STRING      : fragment_type="STRING"
                    elif code[5]==bytecode.TOKEN_TYPE_COMMENT     : fragment_type="COMMENT"
                    elif code[5]==bytecode.TOKEN_TYPE_WHITESPACE  : fragment_type="WHITESPACE"
                    elif code[5]==bytecode.TOKEN_TYPE_EXPRESSION  : fragment_type="EXPRESSION"
                    elif code[5]==bytecode.TOKEN_TYPE_OTHER       : fragment_type="OTHER"
                    elif code[5]==bytecode.TOKEN_TYPE_KEYWORD     : fragment_type="KEYWORD"
                    elif code[5]==bytecode.TOKEN_TYPE_RESERVED    : fragment_type="RESERVED"
                    elif code[5]==bytecode.TOKEN_TYPE_NUMERIC     : fragment_type="NUMERIC"
                    elif code[5]==bytecode.TOKEN_TYPE_OPERATOR    : fragment_type="OPERATOR"
                    elif code[5]==bytecode.TOKEN_TYPE_DELIMITER   : fragment_type="DELIMITER"
                    elif code[5]==bytecode.TOKEN_TYPE_FUNCTION    : fragment_type="FUNCTION"
                    
                    bc='0x{0:04x}'.format(code[1])
                    if code[1]==0:
                        bc='      '
                    
                    print("{0:20} | {1} | {2}     | {3:10}  | {4:4}        | {5:13}        | {6:3}   | {7}".format(word,bc,code[2],code[3],code[4],fragment_type,error,level))

##
## End bytecode class
##





# calls the bytecode class and converts the sql into a list of integers and strings
# which are pattern matched
class lexer:
    bytecode_index=0
    bytecode_length=0
    bytecode_id=0
    _offset=None
    _length=None
    _from  =None
    _joins =[]
    
    def __init__(self,cmd_text,debug=True):
        print ("LEXER")
        self.bytecode,self.bytecode_id=bytecode.get_BYTECODE(cmd_text)
        print ("BYTECODE")
        self.bytecode_length=len(self.bytecode)
        if debug: bytecode.print_code(self.bytecode) 

        print ("LEX")
        self.process_bytecode(bytecode)

    

    def get_next_bytecode(self):
        if isinstance(codes,list):
            for code in codes:
                if isinstance(code,dict):
                    bytecode.print_code(code['sub'],None)
        
    def pin_index(self):
        self.bytecode_index_pin=self.bytecode_index

    def resetpin_index(self):
        self.bytecode_index=self.bytecode_index=pin

    def validate_match_set(self,results):
        for result in results:
            if result==None:
                return None
        return retults

    def match(self,pattern,optional=None):
        found=None
        bytecode_index=self.bytecode_index
        for sequence in  pattern:
            if bytecode_index>=self.bytecode_length:
                break
            pattern_match=None
            if isinstance(sequence,int):
                print sequence,self.bytecode[bytecode_index]
                if self.bytecode[bytecode_index][1]==sequence:
                    print ("match {0}".format(sequence))
                    pattern_match=True
                    found=[]

            if None==pattern_match:
                raise Exception("Pattern not found, PRE")        

            bytecode_index+=1
        
        if found!=None:
            self.bytecode_index=bytecode_index
            return found
        if optional:
            self.bytecode_index=bytecode_index
            return None
        raise Exception ("No Match")
    
    # atleast 1 thing must be matched, or it fails
    def match_or(self,patterns):
        for pattern in patterns:
            try:
                return self.match(pattern)
            except:
                pass
        raise Exception ("No or Match")

    def process_bytecode(self,bytecode):
        self.bytecode_index=0
        while self.bytecode_index<self.bytecode_length:
            old_bytecode_index=self.bytecode_index
            self.keyword_select()
            if self.bytecode_index==old_bytecode_index:
                raise Exception("Not found")
    
    def keyword_select(self):
        try:
            self.match([bytecode.SELECT])
        except Exception as ex:
            print ex
            return

        self.simple_expression()
        self.keyword_FROM()
        self.keyword_JOIN()
        self.keyword_LEFT_JOIN()
        self.keyword_RIGHT_JOIN()
        self.keyword_FULL_JOIN()
        self.keyword_OUTER_JOIN()
        self.keyword_INNER_JOIN()
        self.keyword_WHERE()
        self.keyword_ORDER_BY()
        self.keyword_GROUP_BY()
        self.keyword_LIMIT()

    def simple_expression(self):
        pass

    def keyword_FROM(self):
        try:
            self._from= self.match([bytecode.FROM,'F']) 
        except:
            pass

    def keyword_JOIN(self):
        try:
            self._joins.append(self.match([bytecode.JOIN]) )
        except:
            pass

    def keyword_LEFT_JOIN(self):
        try:
            self.joins.append(self.match([bytecode.LEFT,bytecode.JOIN]) )
        except:
            pass
        pass

    def keyword_RIGHT_JOIN(self):
        self._joins.append(self.match([bytecode.RIGHT,bytecode.JOIN]) )
        pass

    def keyword_FULL_JOIN(self):
        self._joins.append(self.match([bytecode.FULL,bytecode.JOIN]) )
        pass

    def keyword_OUTER_JOIN(self):
        pass

    def keyword_INNER_JOIN(self):
        pass

    def keyword_WHERE(self):
        pass

    def keyword_ORDER_BY(self):
        pass

    def keyword_GROUP_BY(self):
        pass

    def keyword_LIMIT(self):
        try:
            self._offset,self._length= match([K_LIMIT,'I,I']) 
        except:
            try:
                self._length         = match([K_LIMIT,'I']) 
            except:
                pass




    def bit_expression(bytecode):
        try:
            self.bit_expr()
            self.match(bytecode.O_OR)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_AND)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_LEFT_SHIFT)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_RIGHT_SHIFT)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_PLUS)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_MINUS)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_MULTIPLY)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_DIVIDE)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.DIV)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.MOD)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_MODULUS)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.XOR)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_PLUS)
            self.interval_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_MINUS)
            self.interval_expr()
        except:
            pass

        try:
            self.simple_expr()
        except:
            pass
        raise Exception("No BIT_EXPR")
        # time intercal expression

    def interval_exp(self):
        try:
            self.match(bytecode.INTERVAL)
        except:
            raise exception("Not an interval")

        patterns=[
            [bytecode.INTERVAL,INT                                   , bytecode.MICROSECONDS],
            [bytecode.INTERVAL,INT                                   , bytecode.SECOND],
            [bytecode.INTERVAL,INT                                   , bytecode.MINUTE],
            [bytecode.INTERVAL,INT                                   , bytecode.HOUR],
            [bytecode.INTERVAL,INT                                   , bytecode.DAY],
            [bytecode.INTERVAL,INT                                   , bytecode.WEEK],
            [bytecode.INTERVAL,INT                                   , bytecode.MONTH],
            [bytecode.INTERVAL,INT                                   , bytecode.QUARTER],
            [bytecode.INTERVAL,INT                                   , bytecode.YEAR],
            [bytecode.INTERVAL,[INT,DOT,INT                        ] , bytecode.SECOND_MICROSECOND],
            [bytecode.INTERVAL,[INT,COLON,INT,DOT,INT              ] , bytecode.MINUTE_MICROSECOND],
            [bytecode.INTERVAL,[INT,COLON,INT                      ] , bytecode.MINUTE_SECOND],
            [bytecode.INTERVAL,[INT,COLON,INT,COLON,INT,DOT,INT    ] , bytecode.HOUR_MICROSECOND],
            [bytecode.INTERVAL,[INT,COLON,INT,COLON,INT            ] , bytecode.HOUR_SECOND],
            [bytecode.INTERVAL,[INT,COLON,INT                      ] , bytecode.HOUR_MINUTE],
            [bytecode.INTERVAL,[INT,INT,COLON,INT,COLON,INT,DOT,INT] , bytecode.DAY_MICROSECOND],
            [bytecode.INTERVAL,[INT,INT,COLON,INT,COLON,INT        ] , bytecode.DAY_SECOND],
            [bytecode.INTERVAL,[INT,INT,COLON,INT                  ] , bytecode.DAY_MINUTE],
            [bytecode.INTERVAL,[INT,INT                            ] , bytecode.DAY_HOUR],
            [bytecode.INTERVAL,[INT,DASH,INT                       ] , bytecode.YEAR_MONTH],
        ]

        for pattern in patterns:
            results=self.match(pattern)
            if results:
                return results
        raise Exception("Not a interval Expression")    # comparitors

    def comparison_operator(self): 
     # TOD  <> OR !=... fix
     return self.match_or([EQUALS,OR,GREATER_EQ,GREATER,LESS_EQ,LESS,NOT_EQ])

    def expression(self):
        try:
            self.expr()
            self.match(bytecode.OR)
            self.expr()
        except:
            pass

        try:
            self.expr()
            self.match(bytecode.SHORT_CIRCUIT_OR)
            self.expr()
        except:
            pass

        try:
            self.expr()
            self.match(bytecode.XOR)
            self.expr()
        except:
            pass


        try:
            self.expr()
            self.match(bytecode.AND)
            self.expr()
        except:
            pass

        try:
            self.expr()
            self.match(bytecode.SHORT_CIRCUIT_AND)
            self.expr()
        except:
            pass

        try:
            self.match(bytecode.NOT)
            self.expr()
        except:
            pass
        
        try:
            self.match(bytecode.NEGATE)
            self.expr()
        except:
            pass
        
        try:
            self.boolean_primary()
            self.match(bytecode.IS) 
            self.match(bytecode.NOT,optional=True)
            self.match_or([bytecode.TRUE,bytecode.FALSE,bytecode.UNKNOWN])
        except:
            pass

        try:
            self.boolean_primary()
        except:
            pass

        raise Exception ("No Expression")
   
    def boolean_primary(self):
        try:
            self.boolean_primary()
            self.match(bytecode.IS)
            self.match(bytecode.NOT,optional=True)
            self.match(bytecode.NULL)
        except: 
            pass
        
        try:
            self.boolean_primary()
            self.match(bytecode.NULL_EQ)
            self.predicate()
        except:
            pass
    
        try:
            self.boolean_primary()
            self.comparison_operator()
            self.predicate()
        except:
            pass

        try:
            self.boolean_primary()
            self.comparison_operator()
            self.predicate()
        except:
            pass
        try:
            self.boolean_primary()
            self.comparison_operator()
            # {ALL | ANY}
            self.match_or([bytecode.ALL,bytecode.ANY],optional) 
            self.subquery()
        except:
            pass
        try:
            self.predicate()
        except:
            pass
        raise Exception("No boolean primary")
 
    def predicate(self):
        try:
            self.bit_expr()
            self.match(bytecode.NOT,OPTIONAL)
            self.match(bytecode.IN)
            self.subquery()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.NOT,optional=True)
            self.match(bytecode.IN)
            self.expr_array()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.NOT,optional=True)
            self.match(bytecode.BETWEEN)
            self.bit_expr()
            self.match(bytecode.AND)
            self.predicate
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.SOUNDS,bytecode.LIKE)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.NOT,optional=True)
            self.match(bytecode.LIKE)
            self.simple_expr()
            try:
                results=self.match(bytecode.ESCAPE,optional=True)
                if results:
                    self.simple_expr()
            except:
                raise Exception("Escape syntax")
        except:
            pass

        try:
            self.bit_expr()
            self.match(sbytecode.NOT,optional=True)
            self.match(bytecode.REGEXP)
            self.bit_expr()
        except:
            pass

        try:
            return self.bit_expr()
        except:
            pass
        raise Exception ("No predicate")

    def colation_name(self):
        return self.match_OR([bytecode.COLATION_DATABASE_DEFAULT,bytecode.COLATION_UTF8])

    # strig or numeric literal
    def literal(self):
        if is_instance(self.bytecode[self.bytecode_index],str):
            return True
        raise Exception("Not Literal")


    # TODO
    def identifier(self):
        return True

    def function_call(self):
        return True

    def param_marker(self):
        return True

    def variable(self):
        return True

    def expr_array(self):
        return True
    
    def subquery(self):
        return True        
    
    def match_expr(self):
        return True
    
    def case_expr(self):
        return True
    

    def simple_expr(self):
        # sets the restart pointer for the bytecode index
        self.pin_index()
        
        try:   
            self.resetpin_index()
            return { self.literal() }
        except: 
            pass
        
        try:    
            self.resetpin_index()
            return { self.identifier() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.function_call() }
        except: 
            pass
        
        try:    
            self.resetpin_index()
            return { self.simple_expr(),self.match(bytecode.COLLATE),self.colation_name() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.param_marker() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.variable() }
        except: 
            pass
        
        try:    
            self.resetpin_index()
            return { self.simple_expr() , self.match(bytecode.O_SHORTCIRCUIT_OR) , self.simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.O_PLUS)  , simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.O_MINUS) , simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.O_NOT)   , simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.O_NEGATE), simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.BINARY)  , simple_expr() }
        except: 
            pass
        
        try:    
            self.resetpin_index()
            return { self.expr_22 }
        except: 
            pass
        
        # I dont really know what the ROW(expr[,expr ...]) does
        #try:    
        #    self.resetpin_index()
        #    return { self.match(self.bytecode.ROW), (,self.expr_array()) }
        #except: 
        #    pass

        try:    
            self.resetpin_index()
            return { self.subquery() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(bytecode.EXISTS) ,self.subquery() }
        except: 
            pass
        

        try:    
            self.resetpin_index()
            return { self.identifier(),self.expr() }  # {}? }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match_expr() }
        except: pass

        
        try:    
            self.resetpin_index()
            return { self.case_expr() }
        except: pass

        
        try:     
            self.resetpin_index()
            return { self.interval_expr() }
        except:  pass

        # nothing matched. 
        self.resetpin_index()
        

# PASS 1 TOKENIZE, and identify
# pass 2 pattern match
# pass 3 error handle
# identfiyers not required after "." on quoted identifyer or valid...thing like DB something (l;ook up again)

def test(debug=None):
    query="""
    select COUNT(*) AS number,*,(SELECT first_name FROM test.mock LIMIT 1) as first_name
    FROM test.mock 
    WHERE first_name='bob' 
    and last_name not 'sam' 
    and gender=F 
    and last_name in (SELECT last_name FROM test.mock LIMIT 10 WHERE last_name like '%sam%') as first_name
    
    -- this is a comment
    -- this is another comment /* */ fe
    -- this is also a comment 'quote'
    -- this is also a comment "double quote"
    ;
    b=:('rewrew')
    /*
        Block Comment #1
    */
        """
    lexer(query)
    #codes=bytecode.get_BYTECODE(query)
    #if debug: bytecode.print_code(codes) 


#print(timeit.timeit(test, number=10))

test(True)




# Rules....
# 
# 
# 
# RESERVED words do not use quotes or filed identifiers
# Keywords MUST use field identifiers -> ` <-

# 
# 
# 
# 
# 
# if the word is a keyword, congert to bytecode
# if the word isnt, store as string
