import sys
from collections import OrderedDict




class record_configuration:
    __slots__=()  
    # data
    columns               = None
    column_count          = 0
    line_number           = None
    data_starts_on_line   = 0
    remove_block_quotes   = None
    render_whitespace     = None
    render_comment        = None
    comment_delimiter     = '#'
    field_delimiter       = ','
    block_quote_delimiter = "'"
    # class pointers
    meta                  = None
    context               = None

    def __init__(self):
        pass



class record:
    __slots__=()
    __internal={'__type'        : 0,
              '__raw'         : None,
              '__line_number' : None,
              '__error'       : None,
              '__match'       : None
              }
    
    __data=OrderedDict()

    def __init__(self, data, config):
        self.__raw         = data
        self.__line_number = config.line_number

        # create empty dataset for row
        for column in config.columns:
            self.__data[column]=None

        # process string into dataset
        self.process( data, config)
      
    def __getattr__(self, name):
        try:
          if   name=='_record__type':        return self.__internal['__type']
          elif name=='_record__raw':         return self.__internal['__raw']
          elif name=='_record__line_number': return self.__internal['__line_number']
          elif name=='_record__error':       return self.__internal['__error']
          elif name=='_record__match':       return self.__internal['__match']
          elif name=='_record__data':        return self.__internal['__data']
          else:
              return self.__data[name]
        except :
            err_msg="Key not valid: '{0}'".format(name)
            raise Exception (err_msg)

    def __setattr__(self, name, value):
        if   name=='_record__type':        self.__internal['__type']       =value
        elif name=='_record__raw':         self.__internal['__raw']        =value
        elif name=='_record__line_number': self.__internal['__line_number']=value
        elif name=='_record__error':       self.__internal['__error']      =value
        elif name=='_record__match':       self.__internal['__match']      =value
        elif name=='_record__data':        self.__internal['__data']       =value
        else:
          if self.__data.has_key(name)==False:
             err_msg="Cannot assign data to invalid key: '{0}'".format(name)
             raise Exception (err_msg)

          try:
                self.__data[name]=value
          except :
              err_msg="Cannot assign data to Key: '{0}'".format(name)
              raise Exception (err_msg)

    def __delattr__(self, name):
        try:
            del self.__data[name]
        except :
            err_msg="Cannot delete key: '{0}'".format(name)
            raise Exception (err_msg)

    def __iter__(self):
        for key in self.__data:
            yield key

    def keys(self):
      return self.__data.keys()

    def has_key(self,key):
      return self.__data.has_key(key)

    # PY3 support
    def items(self):
        for key in self.__data:
          yield key, self.__data[key]

    # PY2 support
    def iteritems(self):
        for key in self.__data:
          yield key, self.__data[key]

    def split_array(self,arr):
        ARRAY_DELIMITER=','
        TUPEL_DELIMITER='='
        
        split=arr.split(ARRAY_DELIMITER)
        
        store={}
        for item in split:
          try:
            setting_key,setting_value=item.split(TUPEL_DELIMITER)
            store[setting_key]=setting_value
          except:
            store[item]=item

          kv=self.split_key_value(item)
          store.append(kv)
        
        if len(store)==1:
          return store[0]
        strings=0
        dicts=0
        for item in store:
          if isinstance(item,str):
            strings+=1
          elif isinstance(item,dict):
            dicts+=1
        
        # they are all dicts combine
        if dicts>=0 and strings==0:
          store2={}
          for item in store:
            store2.update(item)
          store=store2

        return store
     
    def split_key_value(self,blob):
        try:
          setting_key,setting_value=blob.split('=')
          return {setting_key:setting_value}
        except:
          pass
        return blob

    def process_rows(self,set,prefix):
          res={}
          for row in set.data:
            data=row['data']
            for key in data:
                self.split_array(value)
          return res

    def process(self, data, config):
        COMMENT     = 0
        WHITESPACE  = 1
        DATA        = 2
        
        match               = None
        data_type           = DATA
        error               = None
        #Determine line type
        try:
            if data[0]==config.comment_delimiter:
   en(temp_data_file, 'rb', buffering=0)
        try:
            dst             data_type=COMMENT
            elif config.data_starts_on_line <config.line_number:
                data_type=COMMENT
                if config.render_comment:
                    match=True
            elif not data:
                data_type=WHITESPACE
                if config.render_whitespace:
                    match=True
        # FAIL TO COMMENT
        except:
            data_type=COMMENT
            if config.render_comment:
                match=True

        #if its actual data. lets split it and make some structures
        if data_type==DATA:
            tokens=data.split(config.field_delimiter, config.column_count)
            #print tokens
            if config.remove_block_quotes:
                i=0
                for token in tokens:
                    if len(token)>1 and token[0] == config.block_quote_delimiter and token[-1] == config.block_quote_delimiter:
                            token=token[1:-1]
                    column_name=config.columns[i]
                    self.__data[column_name]=token
                    i+=1
            else:
                i=0
                for token in tokens:
                    column_name=config.columns[i]
                    self.__data[column_name]=token
                    i+=1
        
        # SET data statistics, non iterable
        self.__type        = data_type
        self.__error       = error
        self.__match       = match


#        # If no where. return everything
#        if 'where' not in query_object['meta']:
#            match_results = True
#        else:
#            # if a where, only return data, comments/whites/space/errors are ignored
#            
#            if line_type == context.data_type.DATA:
#                match_results = context.match.evaluate_match(context,query_object, line_data)
#            else:
#                match_results = False
#        

#    has_columns = select_has_columns(context,meta)
#    has_functions = select_has_functions(context,meta)
#    table=None
#    line_number = 1
#    data=[]
#    if True == has_columns:
#        if meta.table:
#            table= meta.table
#        else:
#            raise Exception ('table configuration has no data file')
        

            
#    def get_first(self):
#        try:
#            return self.data[0]['data'][0]
#        except:
#            pass
#        return None
#
#    def is_single(self):
#        try:
#            if len(self.data)==1:
#                return True
#        except:
#            pass
#        return None


class table:
    __slots__=()
    
    config             =None
    rows               =None
    success           = None
    affected_rows     = None
    diff              = None
    error             = None
    total_data_length = None
    delimiter         = None
    new_line          = None
    data_length       = None
    columns           = None
    column_length     = None

    def __init__(self,context,meta):
        self.init_record_config(context,meta)
    
    # sets up the per record config data
    def init_record_config(self,context,meta):
        config=record_configuration()
        config.line_number           = 0
        config.data_starts_on_line   = meta.table.data.starts_on_line
        config.column_count          = meta.table.column_count()
        config.field_delimiter       = meta.table.delimiters.field
        config.render_whitespace     = meta.table.visible.whitespace
        config.render_comments       = meta.table.visible.comments
        config.render_errors         = meta.table.visible.errors
        config.remove_block_quotes   = None
        config.block_quote_delimiter = "'"
        config.meta                  = meta
        config.context               = context
        self.config=config
    
    def update_statistics(self):
        self.success           = None
        self.affected_rows     = None
        self.diff              = None
        self.error             = None
        self.total_data_length = None
        self.delimiter         = None
        self.new_line          = None
        self.columns           = None
        self.data_length       = None
        self.column_length     = None

    def load(self):
        # prep data
        data=[]
        self.rows=None

        # file reads from a sourced copy of the data file
        # a manager regulates the creation and vending of this file
        temp_data_file=self.config.context.get_data_file(self.config.meta.table)

        # loop through file as fast as possible
        with open(temp_data_file, 'r') as content_file:
            line_number=0
            for line in content_file:
                self.config.line_number=line_number
                data.append(record(line,self.config))
                line_number+=1
        # release lock and swap files if need be.
        self.config.context.auto_commit(self.config.meta.table)
        # return the acumulated data
        self.rows=data
  
    # magic iterate method (for loop)
    def __iter__(self):
        for row  in self.rows:
            yield row


