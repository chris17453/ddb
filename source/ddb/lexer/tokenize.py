# cython: linetrace=True

# yes, this could be a giant regex, but no.
# TODO: memory optimization.. maybe not sure how wastefull this is
class tokenizer:

    def chomp(self,text, discard_delimiters=False, discard_whitespace=True, debug=None):
        self.debug_on = None
        tokens = []

        # clean leading and trailiong stuff
        text = text.strip()
        # visual formatting characters
        whitespace = [' ', '\t', '\n', '\r' ]
        # these are solid non depth related blocks
        blocks = [
            ['\'', '\'', 'quote'],   # string block
            ['"' , '"' , 'quote'],   # string block
            ['[' , ']' , 'db'],   # mssql column
            ['`' , '`' , 'db'],   # mysql column
        ]

        # blocks that must match depth
        # nested_block = [
        #                ['(',')']
        #              ]

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

        # add block identifiers to delimiters
        for b in blocks:
            if b[0] not in delimiters:
                delimiters.append(b[0])
            if b[1] not in delimiters:
                delimiters.append(b[1])

        delimiters_sorted = self.sort_array_by_length(delimiters)

        # padding prevents fencpost error
        #text+=" "
        text_length = len(text)
        # c is the incremental pointer to the string
        word_start = 0
        tokens = []
        c = 0
        #print delimiters_sorted
        delimter_len = 1
        in_block = None
        block = None

        while c < text_length:

            self.info("-", c)
            just_crossed_block = False
            for b in blocks:
                
                # info(b[0],b[1],c,delimter_len)
                fragment = text[c]
                # only check for block start if not in one
                if None == in_block:
                    if fragment==b[0] and fragment is not None:
                        just_crossed_block = True
                        self.info("IN BLOCK", c)
                        in_block = b
                        block = b
                        c += 1
                        self.info("IN BLOCK", c)
                        break
                # check for block end
                else:
                    if block:
                        if (fragment== block[1] and fragment is not None) or c >= text_length - 1:
                            just_crossed_block = True
                            self.info("NOT IN BLOCK", c)
                            in_block = None
                            c += 1
                            break
            # skip stuff in block
            if in_block  is not None:
                self.info("in block skip")
                if not just_crossed_block:
                    c += 1
                continue
            #  equal.. greater than. we want the things on the last pass...
            self.info("position1", c, text_length)
            if c > text_length:
                self.info("Greater than length of text. exiting")

                break
            for d in delimiters_sorted:
                delimter_len = len(d)
                fragment = text[c:c + delimter_len]
                #if c>0 and text[c-1:1].isalpha():
                #    fragment_before_alpha=True
                #else:
                #    fragment_before_alpha=False

                #if c+1<text_length and   text[c+1:1].isalpha():
                #    fragment_after_alpha=True
                #else:
                #    fragment_after_alpha=False
                #    
                #if c >= text_length - 1:
                #    self.info("Last Cycle")

                #if fragment_before_alpha==True  and fragment_after_alpha==True:

                if c >= text_length - 1:
                    end_of_string=True
                else:
                    end_of_string=None
                if (fragment== d and fragment is not None) or end_of_string:
                    if end_of_string:
                        self.info("Delemiter found, end of string", c, fragment)
                    else:    
                        self.info("Delemiter found", c, fragment)
                    if c - word_start > 0:
                        self.info("Data word found", c - word_start)
                        word_end = c
                        if word_end >= text_length-1:
                            self.info("word ends on last character", word_end, text_length)
                            not_delimiter = text[word_start:word_end]
                            fragment=None
                        else:
                            not_delimiter = text[word_start:word_end]
                        
                        token_type = 'data'
                        if block is not None:
                            self.info("HAS BLOCK")
                            block_left = block[0]
                            block_right = block[1]
                            block_type = block[2]
                            block = None
                            not_delimiter = not_delimiter[len(block_left):-len(block_right)]
                        else:
                            self.info("NO  BLOCK")
                            block_left = None
                            block_right = None
                            block_type = None
                        self.info("POSITION", c, not_delimiter)
                        # if not not_delimiter:
                        #    break

                        tokens.append({'type': token_type, 'data': not_delimiter, 'block_left': block_left, 'block_right': block_right, 'block_type': block_type})

                    self.info("After Data Append, Position", c, 'of', text_length)
                    # if  c>=text_length-1:
                    #   info("Break, after end of string",c)
                    #   break

                    word_start = c + delimter_len

                    if not fragment or fragment == '':
                        break
                    if True == discard_whitespace and fragment in whitespace:
                        break

                    # if True == discard_delimiters:
                    #     continue

                    delimiter_type = "delimiter"
                    if fragment in operators:
                        delimiter_type = 'operator'
                    else:
                        if fragment in whitespace:
                            delimiter_type = 'whitespace'

                    self.info("delemiter c/fragment- ", c, fragment)
                    tokens.append({'type': delimiter_type, 'data': fragment.lower()})

                    break
            c += delimter_len
        self.debug_on=True
        if True == self.debug_on:
            self.info("-[Tokens]----------------")
            for t in tokens:
                self.info("  -{0}".format(t['data']) )
            self.info("-[End-Tokens]------------")
        return tokens


    def compare_text_fragment(self,x, y):
        if None == x or None == y:
            return False
        if x == y:
            return True
        return False


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
            if arg3 is None and arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return
            if arg3 is None:
                print("{0} {1} {2}".format(msg, arg1, arg2))
                return
            if arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return
            if arg1 is None:
                print("{0}".format(msg))
                return

            print("[{0}]".format(msg))

