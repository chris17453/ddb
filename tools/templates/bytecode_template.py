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
    def add_fragment(fragment,fragment_length,uid,fragment_id,bulk=None,depth=0):
        new_fragments=[]
        if bulk:
            if fragment!="":
                new_fragments.append([fragment,0,depth,uid,fragment_id])
        else:
            if fragment!="":
                right_fragment=""
                right_fragment_length=0
        
                while fragment_length>0:
                    found=None
                    for length in xrange(fragment_length,0,-1):
                        code=bytecode.get_intermediate_code_2(fragment[:length])
                        if code!=0:
                            found=True
                            if code==bytecode.SPACE or code==bytecode.TAB or code==bytecode.NEW_LINE or code==bytecode.COMMA:
                                pass
                            else:
                                new_fragments.append([fragment[:length],code,depth,uid,fragment_id])
                            fragment_length-=length
                            if fragment_length>0:
                                fragment=fragment[length:]
                            break;
                    
                    # if we looped through all length combiniations and found nothing, add the remainder and shrink the stack
                    if found==None:
                        new_fragments.append([fragment[0],0,depth,uid,fragment_id])
                        fragment_length-=1
                        if fragment_length>0:
                            fragment=fragment[1:]
        
        return new_fragments
   
    @staticmethod
    def get_BYTECODE(data,depth=0,uid="1"):
        fragments=[]
        fragment=""
        fragment_length=0
        in_block=None
        in_alpha=None
        block_depth=0
        fragment_id=1
        # main loop for tokenizing
        for c in data:
            
            if in_block:
                in_alpha=None
                # is it the other side of the block
                if c==bytecode.LEFT_PAREN_STR:      
                    block_depth+=1
                    fragment+=c
                    fragment_length+=1
                    continue
    
                if c==in_block:
                    
                    if in_block==bytecode.RIGHT_PAREN_STR:
                        block_depth-=1
                        if block_depth!=0:
                            fragment+=c
                            fragment_length+=1
                            continue

                        sub_code=bytecode.get_BYTECODE(fragment,depth+1,"{0}.{1}".format(uid,fragment_id))
                        fragments+=sub_code
                    else:
                        fragment_id+=1
                        fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,True,depth)
                    fragment=""
                    fragment_length=0
                    in_block=None
                # no, add the contents
                else:
                    fragment+=c
                    fragment_length+=1
            else:
                # self closing
                if   c==bytecode.DOUBLE_QUOTE_STR:    in_block=bytecode.DOUBLE_QUOTE_STR
                elif c==bytecode.SINGLE_QUOTE_STR:    in_block=bytecode.SINGLE_QUOTE_STR
                elif c==bytecode.BACK_TIC_STR:        in_block=bytecode.BACK_TIC_STR
                
                # matched pair
                elif c==bytecode.LEFT_COMMENT_STR:    in_block=bytecode.RIGHT_COMMENT_STR
                elif c==bytecode.COMMENT_SINGLE_STR:  in_block=bytecode.NEW_LINE_STR
                elif c==bytecode.LEFT_PAREN_STR:      
                    in_block=bytecode.RIGHT_PAREN_STR
                    block_depth+=1
        
                if in_block:
                    fragment_id+=1
                    fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,None,depth)
                    fragment=""
                    fragment_length=0
                    continue
                    
                #not a block, or anything else
                else:
                    # is this the start of an "WORD"
                    u_alpha   =c>=bytecode.A_STR and c<=bytecode.Z_STR
                    l_alpha   =c>=bytecode.a_STR and c<=bytecode.z_STR 
                    numeric   =c>=bytecode.ZERO_STR and c<=bytecode.NINE_STR
                    underscore=c==bytecode.UNDERSCORE_STR 
                    dollar    =c==bytecode.DOLLAR_STR

                    if in_alpha==None:
                        if u_alpha or l_alpha or numeric or underscore or dollar:
                            fragment_id+=1
                            fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,in_alpha,depth)
                            fragment=c
                            fragment_length=1
                            in_alpha=True
                            continue    
    
                    # Are we in a "WORD"
                    else:
                        # If we just LEFT ... add the existing word, and start a new one
                        if not u_alpha and not l_alpha and not numeric and not underscore and not dollar:
                            fragment_id+=1
                            fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,True,depth)
                            fragment=c
                            fragment_length=1
                            in_alpha=None
                            continue    

                    # fallthrough
                    fragment+=c
                    fragment_length+=1

        # END Loop                
        # if anything is still left in the pipeline, cleanup
        
        fragment_id+=1
        fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,in_alpha,depth)
        fragment=""
        fragment_length=0
    
    
        # err if block mismatch
        if in_block:
            err_msg="Missing {0}".format(in_block)
            raise Exception(err_msg)
        
        # reduce groups that are single elements
        #while len(fragments)==1:
        #    print fragments
        #    elif isinstance(fragments,dict):
        #        fragments=fragments['sub']
        #    print fragments
        #    return fragments
        
        return [{"sub":fragments}]

    @staticmethod
    def print_code(codes,root=True):
        if root: print("Token                | Code   | Depth | UID         | Fragment ID ")
        if root: print("---------------------+--------+-------+-------------+-------------")
        if isinstance(codes,list):
            for code in codes:
                if isinstance(code,dict):
                    bytecode.print_code(code['sub'],None)
                elif isinstance(code,list):
                    #for i in range(code[2]):
                    #    print " " , 
                    print("{0:20} | 0x{1:04X} | {2}     | {3:10}  | {4}".format(code[0],code[1],code[2],code[3],code[4]))

    
##
## End bytecode class
##

def test(debug=None):
    query="""SELECT * FROM test.mock WHERE first_name='bob' and last_name not 'sam' and gender=F and last_name in (sam,bob,pizza,chicken) 
        """
    codes=bytecode.get_BYTECODE(query)
    if debug: bytecode.print_code(codes) 


#print(timeit.timeit(test, number=10))

test(True)