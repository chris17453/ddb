# cython: profile=True
# cython: linetrace=True
import sys
import os
from .column import column_v2
from ..output.factory_yaml import yamlf_load, yamlf_dump
from ..file_io.locking import normalize_path
from ..lexer import lexer
# use the c based parser, or you're going to get massive lag with the python based solution


def touch(path):
        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        open(path, 'a').close()

class table:
    def __init__(self,
                 table_config_file=None,
                 database         =None,
                 columns          =None,
                 name             =None,
                 data_file        =None,
                 field_delimiter  =None,
                 config_directory =None,
                 comments         =None,
                 whitespace       =None,
                 errors           =None,
                 data_on          =None,
                 fifo             =None,
                 repo             =None,
                 strict_columns   =None,
                 mode             =None
                 ):
        self.version = 1
        self.ownership = table_ownership()
        self.delimiters = table_delimiters()
        self.visible = table_visible_attributes()
        self.data = table_data(name=name, database=database)
        self.columns = []
        self.active = True
        self.ordinals = {}
        self.ordinal_lookup = {}
        self.errors = []
        self.results = []
        self.config_directory = config_directory

        self.update(data_file=data_file,
                    columns=columns,
                    field_delimiter=field_delimiter,
                    comments=comments,
                    whitespace=whitespace,
                    errors=errors,
                    data_on=data_on,
                    fifo=fifo,
                    repo=repo,
                    strict_columns=strict_columns,
                    mode=mode

                    )

        self.update_ordinals()
        if self.data.path:
            if repo==None:
                if False == os.path.exists(normalize_path(self.data.path)):
                    # no file exists.. create it
                    try:
                        touch(self.data.path)
                        # add a default header, csv safe 
                        with open(self.data.path,"a") as new_file:
                            column_text=[]
                            for column in self.data.columns:
                                column_text.append(column.data.display.name)
                            header="# {0}\n".format(self.delimiters.field.join(column_text) )
                            new_file.write(header )
                        print ("header")
                    except Exception as ex:
                        print("Create Table Error: {0}".format(ex))

        #data:
        #    self.name = None
        #    self.type = "string"
        #    self.is_array = False
        #    self.has_default = False
        #    self.default_value = None
        #    self.ordinal = -1
        #    self.export = False
        #    self.regex = None
        #display
        #    self.name = None
        #    self.ordinal = -1
        #    self.visible = True
        #    self.fixed_width = True
        #    self.width = 100
        #    self.max_width = 0
        #    self.min_width = 0
        #    self.overflow = False
        #search
        #    self.searchable = False
        #    self.multi_search = False
        #sort: sortable = False
        #self.ordinal = 0
        #self.default = False
        #self.default_asc = False




                    #raise Exception("Data file invalid for table: {}, path:{}".format(self.data.name, self.data.path))
                    #self.active = False

    

    def update( self,
                columns         =None,
                data_file      =None,
                field_delimiter=None,
                comments=None,
                whitespace=None,
                errors=None,
                data_on=None,
                fifo=None,
                repo=None,
                strict_columns=None,
                mode=None
                ):
        
        if strict_columns:
            self.data.strict_columns=strict_columns

        if fifo:
            self.data.fifo=fifo
        if data_on:
            #print("SETTING DATA INT",data_on,int(data_on))
            self.data.starts_on_line = data_on
        if comments:
            self.visible.comments = comments

        if whitespace:
            self.visible.whitespace = whitespace

        if errors:
            self.visible.errors = errors

        if field_delimiter:
            self.set_field_delimiter(field_delimiter)

        if data_file:
            self.data.path = data_file

        if mode:
            self.data.mode = mode

        if repo:
            if repo.protocol=='svn':

                self.data.path=os.path.join(repo.directory,repo.file)
                self.data.repo_type=repo.protocol
                self.data.repo_url=repo.url
                self.data.repo_user=repo.user
                self.data.repo_password=repo.password
                self.data.repo_dir=repo.directory
                self.data.repo_file=repo.file
                
        if columns:
            self.columns = []
            for column in columns:
                self.add_column(column)


    def set_field_delimiter(self, delimiter):
        self.delimiters.field = delimiter

    def append_data(self, data):
        """Add a row to the resultset for this table"""
        self.results.append(data)

    def column_count(self):
        """Return the column count for this table"""
        return self.column_length

    def get_columns(self):
        """return a list of columns"""
        columns = []
        for column in self.columns:
            columns.append(column.data.name)
        return columns

    def get_columns_display(self):
        """return a list of columns with alternate display name"""
        columns = []
        for column in self.columns:
            if None != column.display.name:
                columns.append(column.display.name)
            else:
                columns.append(column.data.name)
        return columns

    def get_results(self):
        columns = self.get_columns_display()
        return {'columns': columns, 'results': self.results}

    def results_length(self):
        """Return the result set length for this table"""
        return len(self.results)

    def error_count(self):
        """Return the result set length for this table"""
        return len(self.errors)

    def add_error(self, error):
        """Add an error to the list of errors processed this cycle"""
        self.errors.append(error)

    def add_column(self, name, display=None):
        """Add a column to this table"""
        column = column_v2()
        column.data.name = name
        column.display.name = display
        self.columns.append(column)
        self.column_length=len(self.columns)
        self.update_ordinals()

    def get_column_at_data_ordinal(self, ordinal):
        for c in self.columns:
            if c.data.ordinal == int(ordinal):
                return c.data.name
        return None

    def has_column(self, column):
        """determine if a column exists by string name"""
        if column == '*':
            return True
        for c in self.columns:
            if column == c.data.name:
                return True
        return False

    def get_ordinal_by_name(self, name):
        for c in self.columns:
            if c.data.name == name:
                return c.data.ordinal
        return None

    def column_ordinals(self):
        temp_columns = []
        for c in self.columns:
            if c.display.visible:
                temp_columns.append(
                    {'data': c.data.ordinal, 'display': c.display.ordinal})

        #L = [(k,v) for (k,v) in temp_columns]
        # temp_columns=sorted(L,key=lambda (k,v): v['display'])  # change to data to sort by data
        return temp_columns

    def does_data_ordinal_exist(self, ordinal):
        for c in self.columns:
            if int(c.data.ordinal) == ordinal:
                return True
        return False

    def get_lowest_available_ordinal(self):
        for c in range(0, len(self.columns)):
            if False == self.does_data_ordinal_exist(c):
                return c
        return None

    def get_column_by_name(self, name):
        for c in self.columns:
            if c.data.name == name:
                return c

    def get_data_by_name(self, name, row):
        try:
            index=self.ordinals[name]
            return row[index]
        except:
            raise Exception("Data Error")
                
        #for c in self.columns:
        #    if c.data.name == name:
        #        i = c.data.ordinal
        #        if None == row:
        #            return None
        #        if len(row) <= i:
        #            return None
        #        return row[i]

    def get_data_from_column(self, column, row):
        i = column.data.ordinal
        if None == row:
            return None
        if len(row) <= i:
            return None
        return row[i]

    def update_ordinals(self):
        if None == self.columns:
            return

        column_count = len(self.columns)
        #has_ordinal=[i for i in range(column_count)]

        self.ordinals = {}
        for k, v in enumerate(self.columns):
            if None == v.data.ordinal or -1 == v.data.ordinal:

                #print (self.columns[k].data.ordinal)
                self.columns[k].data.ordinal = self.get_lowest_available_ordinal()
                self.ordinals[v.data.name] = self.columns[k].data.ordinal
            else:
                self.ordinals[v.data.name] = v.data.ordinal

        # create lookup hash
        # for i in range (0,column_count):
        #    has_ordinal[i]=False
#
        # index=0
        # for c in self.columns:
        #    c.data.ordinal=index
        #    display_ordinal=c.display.ordinal
        #    display_visible=c.display.visible
        #    index+=1
        #
        #    if True == display_visible and  -1 < display_ordinal and display_ordinal < column_count:
        #        has_ordinal[display_ordinal]=True
        #    else:
        #        c.display.ordinal=-1;
#
        # for oi in range(0,columns_count):
        # for c in self.columns:
        #    column=c
        #    if True == column.display.visible and column.display.ordinal==-1:
        #        for i in range (0,column_count):
        #            if False == has_ordinal[i]:
        #                print(" NEEDS {0,2} - {1} ",format(i,c.data.name))
        #                c.dispaly.ordinal=i
        #                has_ordinal[i]=True
        #                break
        #    else:
        #        print(" HAS   {0,2} - {1}".format(column.ordinal,column.data.name))
    def delete(self):
        try:
            if os.path.exists(self.data.config):
                if os.path.isfile(self.data.config):
                    os.remove(self.data.config)
                
                else:
                    err_msg="Table config is not a file! {1}:{0}:{3}".format(self.data.name,self.data.database,self.data.config)
                    raise Exception (err_msg)
            else:
                err_msg="Table config does not exist! {1}:{0}:{3}".format(self.data.name,self.data.database,self.data.config)
                raise Exception (err_msg)
        except Exception as ex:
            err_msg="Error removing  {1}:{0}:{3}".format(self.data.name,self.data.database,self.data.config)
            raise Exception (err_msg)


    def save(self):
        if None == self.data.name:
            raise Exception("Cannot save a table without a name")

        if None == self.data.database:
            raise Exception("Cannot save a table without a database name")
        self.data.type = "LOCAL"
        # if no config dir given, save in users home dir
        #print self.config_directory
        if None == self.config_directory:
            raise Exception ("No configuration directory")

        if None == self.data.config:
            self.data.config = os.path.join(self.config_directory, "{0}.{1}.table.sql".format(self.data.database,self.data.name))
        
        if len(self.columns)==0:
            raise Exception("No columns in the table. Cant save")
        
        column_str=[]
        for column in self.columns:
            column_str.append("'{0}'".format(column.data.name))
        column_str=",".join(column_str)

        fifo=""
        if self.data.fifo:
            fifo="fifo='{0}'".format(self.data.fifo)

        if self.data.repo_type:
            repo="repo='{0}' url='{1}' user='{2}' password='{3}' repo_dir='{4}' repo_file='{5}'".format(
            self.data.repo_type,
            self.data.repo_url,
            self.data.repo_user,
            self.data.repo_password,
            self.data.repo_dir,
            self.data.repo_file)
        else:
            repo=""

        sql="create table '{0}'.'{1}' ({2}) file='{3}' {9} {10} delimiter='{4}' whitespace={5} errors={6} comments={7} strict={11} data_starts_on={8} ".format(
                self.data.database,
                self.data.name,
                column_str,
                self.data.path,
                self.delimiters.field,
                self.visible.whitespace,
                self.visible.errors,
                self.visible.comments,
                self.data.starts_on_line,
                fifo,
                repo,
                self.data.strict_columns)

        with open(self.data.config,"w") as config_file:
            config_file.write(sql)

        return True


class table_visible_attributes:

    def __init__(self, yaml=None):
        self.comments = False
        self.errors = True
        self.whitespace = False

class table_data:

    def __init__(self, yaml=None, name=None, database=None):
        self.mode = None
        self.type = 'Temp'
        self.name = None
        self.database = 'main'
        self.display_name = None
        self.multi_search = True
        self.starts_on_line = 0
        self.uid = None
        self.path = None
        self.key = None
        self.ordinal = -1
        self.config = None
        self.fifo=None
        self.repo_type=None
        self.repo_url=None
        self.repo_user=None
        self.repo_password=None
        self.repo_dir=None
        self.repo_file=None
        self.strict_columns=False

        if None != name:
            self.name = name

        if None != database:
            self.database = database

     
class table_ownership:

    def __init__(self, yaml=None):
        self.group = None
        self.entity = None
        self.location = None
     

class table_delimiters:

    def __init__(self, yaml=None):
        self.field = ","
        self.array = "|"
        self.error = "#"
        self.block_quote = None
        self.comment = ["#", ";", "/"]
        # TODO hard coding this for a moment... must think
        self.new_line = "\n"

    def get_new_line(self):
        '''Return the correct line ending for the file format'''
        if self.new_line == 'UNIX':
            return '\n'
        elif self.new_line == 'WINDOWS':
            return '\r\n'
        else:
            return '\n'
