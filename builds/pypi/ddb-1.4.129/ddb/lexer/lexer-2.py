import bytecode

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
        self.bytecode_index=self.bytecode_index=self.bytecode_index_pin

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
        bytecode=self.bytecode[self.bytecode_index]
        if bytecode[5]==bytecode.TOKEN_TYPE_BLOCK_STRING or   bytecode[5]==bytecode.TOKEN_TYPE_STRING:
            print ("Literal : {0}".format(bytecode[0]))
            self.bytecode_index+=1
            return self.bytecode[self.bytecode_index]
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
    

    def simple_expression(self):
        # sets the restart pointer for the bytecode index
        self.pin_index()
        
        try:   
            print " Trying Litteral", self.bytecode[self.bytecode_index]
            return { self.literal() }
        except: 
            pass
        
        #try:    
        #    self.resetpin_index()
        #    return { self.identifier() }
        #except: 
        #    pass
#
        try:    
            self.resetpin_index()
            return { self.function_call() }
        except: 
            pass
        #
        #try:    
        #    self.resetpin_index()
        #    return { self.simple_expr(),self.match(bytecode.COLLATE),self.colation_name() }
        #except: 
        #    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.param_marker() }
        #except: 
        #    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.variable() }
        #except: 
        #    pass
        #
        #try:    
        #    self.resetpin_index()
        #    return { self.simple_expr() , self.match(bytecode.O_SHORTCIRCUIT_OR) , self.simple_expr() }
        #except: 
        #    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.match(self.bytecode.O_PLUS)  , simple_expr() }
        #except: 
        #    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.match(self.bytecode.O_MINUS) , simple_expr() }
        #except: 
        #    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.match(self.bytecode.O_NOT)   , simple_expr() }
        #except: 
        #    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.match(self.bytecode.O_NEGATE), simple_expr() }
        #except: 
        #    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.match(self.bytecode.BINARY)  , simple_expr() }
        #except: 
        #    pass
        #
        #try:    
        #    self.resetpin_index()
        #    return { self.expr_22 }
        #except: 
        #    pass
        #
        ## I dont really know what the ROW(expr[,expr ...]) does
        ##try:    
        ##    self.resetpin_index()
        ##    return { self.match(self.bytecode.ROW), (,self.expr_array()) }
        ##except: 
        ##    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.subquery() }
        #except: 
        #    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.match(bytecode.EXISTS) ,self.subquery() }
        #except: 
        #    pass
        #
#
        #try:    
        #    self.resetpin_index()
        #    return { self.identifier(),self.expr() }  # {}? }
        #except: 
        #    pass
#
        #try:    
        #    self.resetpin_index()
        #    return { self.match_expr() }
        #except: pass
#
        #
        #try:    
        #    self.resetpin_index()
        #    return { self.case_expr() }
        #except: pass
#
        #
        #try:     
        #    self.resetpin_index()
        #    return { self.interval_expr() }
        #except:  pass
#
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
