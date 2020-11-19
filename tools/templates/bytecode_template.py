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
                #if c==bytecode.LEFT_PAREN_STR and in_block==bytecode.RIGHT_PAREN_STR:      
                #    block_depth+=1
                #    fragment+=c
                #    fragment_length+=1
                #    continue

                
                temp_test=fragment+c
                in_block_len=len(in_block)
                test_index_length=len(temp_test)
                test_index=test_index_length-in_block_len
                temp_test[test_index:]
                
                
                
                #print '>'+temp_test[test_index:]+'<' 
                #print '>'+in_block+'<' 
                #print '>'+fragment[test_index:]+'.'+in_block
                if test_index_length>=in_block_len and temp_test[test_index:]==in_block:
                         
                    #if in_block==bytecode.RIGHT_PAREN_STR:
                    #    #print 'HI'+fragment+str(block_depth)
                    #    block_depth-=1
                    #    if block_depth!=0:
                    #        fragment+=c
                    #        fragment_length+=1
                    #        continue
                    #    # last character hasnt been added, but maybe others have. pull off the stack
                    #    #if in_block_len>0:
                    #    #    #print len(in_block),fragment+"-EDGE"
                    #    #1    fragment=fragment[0:-1]
                    #    #print fragment +'---'
                    #       
                    #    sub_code=bytecode.get_BYTECODE(fragment,depth+1,"{0}.{1}".format(uid,fragment_id),fragment_id)
                    #    #fragment_id=sub_code[1]['fragment_id']+1
                    #    fragment_id=sub_code[1]
                    #    fragments+=sub_code[0]
                    #else:
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
                #elif c==bytecode.LEFT_PAREN_STR:      
                #    in_block  =bytecode.RIGHT_PAREN_STR
                #    frag_temp =bytecode.TOKEN_TYPE_EXPRESSION
                #    block_depth   +=1
        
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

