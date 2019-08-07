# cython: linetrace=True



class tokenizer:

    def chomp(self,text, discard_delimiters=False, discard_whitespace=True, debug=None):
        self.debug_on = True
        tokens = []

        # clean leading and trailiong stuff
        text = text.strip()
        
        # visual formatting characters
        whitespace = [' ', '\t', '\n', '\r' ]
        # these are solid non depth related blocks
        blocks = [
            ['\'', '\'', 'quote'],   # string block
            ['"' , '"' , 'quote'],   # string block
        ]

        # operators # comparitors
        operators = [
            '&&',  # and short circuit
            '||',  # or short circuit
            '!=',  # Not Equal
            '<>',  # Not Equal
            '<=',  # Less than or equal
            '>=',  # Greater thanbor equal

            '>',  # Greater than
            '<',  # Less than

            '=',  # Equality
            '&',  # and
            '!',  # not
            '|',  # or

            #'not',  # not
            #'is',  # equality
            #'like',  # partial match

            '+',  # addition
            '-',  # subtraction
            '/',  # divide
            '*',  # multiple
            '(',  # left paren   (grouping)
            ')',  # right paren  (grouping)
        ]

        # standard delimiters
        delimiters = [',', '.', ';']

        for token in whitespace:
            delimiters.append(token)

        for token in operators:
            delimiters.append(token)

        string_index=0
        text_length=len(text)
        word=""
        in_block=None
        while string_index<text_length:
            print  text[string_index],string_index
            for block in blocks:
                if in_block:
                    if self.compare(text,string_index,block[1]):
                        print "out block"
                        string_index+=len(block[1])
                        block_word =text[in_block:string_index]
                        block_left =text[in_block]
                        block_right=text[string_index]
                        in_block=None
                        if word!='':
                            tokens.append({'type':'data','block_left':None,'block_right':None,'data':word})
                            word=''

                        tokens.append({'type':'data','block_left':block_left,'block_right':block_right,'data':block_word})
                        
                        break
                else:
                    if self.compare(text,string_index,block[0]):
                        print "in block"
                        in_block=string_index
                        if word!='':
                            tokens.append({'type':'data','block_left':None,'block_right':None,'data':word})
                            word=''
                        break

            if not in_block:
                found=None
                for delimiter in delimiters:
                    
                    if self.compare(text,string_index,delimiter):
                        print "delimiter -{0}-".format(delimiter)
                        if word!='':
                            tokens.append({'type':'data','block_left':None,'block_right':None,'data':word})
                            word=''
                        
                        delimiter_type = "delimiter"
                        if delimiter in operators:
                            delimiter_type = 'operator'
                        else:
                            if delimiter in whitespace:
                                delimiter_type = 'whitespace'

                        if True == discard_whitespace and word in whitespace:
                            pass
                        else:
                            tokens.append({'type':delimiter_type,'block_left':None,'block_right':None,'data':delimiter})

                        string_index+=len(delimiter)
                        found=True
                        break

                if found:    
                    continue
                word+=text[string_index]
            string_index+=1
        if word!='':
            tokens.append({'block_left':None,'block_right':None,'data':word})
            word=''
        
        
        print ("DONE")
        self.info("-[Tokens]----------------")
        for t in tokens:
            self.info("  -{0}-{1}".format(t['data'],t['type']) )
        self.info("-[End-Tokens]------------")     
    
    def compare(self,text,string_index,fragment):
        comparitor=fragment
        comparitor_len=len(comparitor)
        if text[string_index:string_index+comparitor_len]==comparitor:
            return True
        return None
        
    def sort_array_by_length(self,data):
        max_len = -1
        for d in data:
            del_len = len(d)
            if del_len > max_len:
                max_len = del_len

        # make a new array, put them in from longest to shortest, remove dupes
        data_sorted = []
        for i in reversed(range(1, max_len + 1)):
            for d in data:
                if d not in data_sorted:
                    if len(d) == i:
                        data_sorted.append(d)
        return data

    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug_on:
            if arg1 is None:
                print("{0}".format(msg))
                return
            if arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return
            if arg3 is None:
                print("{0} {1} {2}".format(msg, arg1, arg2))
                return

            print("[{0}]".format(msg))


#t=tokenizer()
#t.chomp("select * from sam('bob whats up', 'aaa','ccc','vvv','ffdd') limit 10")
