import sys
import os
from .column import column_v2
from ..output.factory_yaml import yamlf_load,yamlf_dump

# use the c based parser, or you're going to get massive lag with the python based solution


class table:
    def __init__(self,
                    table_config_file=None, 
                    database=None, 
                    columns=None, 
                    name=None, 
                    data_file=None, 
                    field_delimiter=None, 
                    config_directory=None,
                    comments=None,
                    whitespace=None,
                    errors=None,
                    data_on=None
    ):
        self.version = 1
        self.ownership = table_ownership()
        self.delimiters = table_delimiters()
        self.visible = table_visible_attributes()
        self.data = table_data(name=name, database=database)
        self.columns = []
        self.active = True
        self.ordinals = {}
        self.errors = []
        self.results = []
        self.config_directory = config_directory
        self.active=True
        
        self.update(data_file=data_file, 
                    columns=columns, 
                    field_delimiter=field_delimiter, 
                    comments=comments,
                    whitespace=whitespace,
                    errors=errors,
                    data_on=data_on)

        if None != table_config_file:
            if os.path.exists(table_config_file):
                yaml_data = yamlf_load(file=table_config_file)
                # print (yaml_data)
                if None == yaml_data:
                    raise Exception("Table configuration empty")
                #print yaml_data
                for key in yaml_data:
                    if 'version' == key:
                        self.version = yaml_data[key]

                    if 'ownership' == key:
                        self.ownership = table_ownership(yaml=yaml_data[key])

                    if 'delimiters' == key:
                        self.delimiters = table_delimiters(yaml=yaml_data[key])

                    if 'visible' == key:
                        self.visible = table_visible_attributes(yaml=yaml_data[key])

                    if 'data' == key:
                        self.data = table_data(yaml=yaml_data[key])

                    # one offs
                    if 'columns' == key:
                        for c in yaml_data['columns']:
                            # if self.version == 1:
                            #    cv1=column_v1( c )
                            #    cv2=cv1.to_v2()
                            #    self.columns.append( cv2 )
                            # if self.version == 2:
                            self.columns.append(column_v2(c))

                    if 'active' == key:
                        self.active = yaml_data[key]

                    # attr=getattr(self,key)
                    # setattr(self,key,yaml_data[key])

        self.update_ordinals()
        if None != self.data.path:
            if False == os.path.exists(self.data.path):
                #raise Exception("Data file invalid for table: {}, path:{}".format(self.data.name, self.data.path))
                self.active=False

    def update(self,
                    columns=None, 
                    data_file=None, 
                    field_delimiter=None, 
                    comments=None,
                    whitespace=None,
                    errors=None,
                    data_on=None):
        if None != data_on:
            self.data.starts_on_line=int(data_on)
        
        if None != comments:
            self.visible.comments=comments

        if None != whitespace:
            self.visible.whitespace=whitespace

        if None != errors:
            self.visible.errors=errors


        if None != field_delimiter:
            self.set_field_delimiter(field_delimiter)

        if None != data_file:
            self.data.path = data_file

        if None != columns:
            self.columns=[]
            for column in columns:
                self.add_column(column)

    def set_field_delimiter(self, delimiter):
        self.delimiters.field = delimiter

    def append_data(self, data):
        """Add a row to the resultset for this table"""
        self.results.append(data)

    def column_count(self):
        """Return the column count for this table"""
        return len(self.columns)

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
        columns=self.get_columns_display()
        return {'columns':columns,'results':self.results}

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
                temp_columns.append({'data': c.data.ordinal, 'display': c.display.ordinal})

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
        for c in self.columns:
            if c.data.name == name:
                i = c.data.ordinal
                if None == row:
                    return None
                if len(row) <= i:
                    return None
                return row[i]

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

    def save(self):
        if None == self.data.name:
            raise Exception("Cannot save a table without a name")

        if None == self.data.database:
            raise Exception("Cannot save a table without a database name")

        # if no config dir given, save in users home dir
        #print self.config_directory
        if None == self.config_directory:
            home = os.path.expanduser("~")
            # make app dir
            if not os.path.exists(os.path.join(home, '.ddb')):
                os.makedirs(os.path.join(home, '.ddb'))
            home = os.path.join(home, '.ddb')
        else:
            home = self.config_directory

        dest_dir=os.path.join(home, self.data.database)      
        if not os.path.exists(dest_dir):
            #print("Making dest dir {0}".format(dest_dir))
            os.makedirs(dest_dir)

        if None == self.data.config:
            self.data.config = os.path.join(dest_dir, "{0}.ddb.yaml".format(self.data.name))
        #print ("dump:{0}".format(self.data.config))
        yamlf_dump(data=self,file=self.data.config)


class table_visible_attributes:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.comments = False
        self.errors = True
        self.whitespace = False
        if None != yaml:

            if 'comments' in yaml:
                self.comments = yaml['comments']
            if 'errors' in yaml:
                self.errors = yaml['errors']
            if 'whitespace' in yaml:
                self.whitespace = yaml['whitespace']


class table_data:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None, name=None, database=None):
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
        self.retults = None
        if None != name:
            self.name = name

        if None != database:
            self.database = database

        if None != yaml:
            if 'name' in yaml:
                self.name = yaml['name']
            if 'database' in yaml:
                self.database = yaml['database']
            if 'display_name' in yaml:
                self.display_name = yaml['display_name']
            if 'multi_search' in yaml:
                self.multi_search = yaml['multi_search']
            if 'starts_on_line' in yaml:
                self.starts_on_line = int(yaml['starts_on_line'])
            if 'uid' in yaml:
                self.uid = yaml['uid']
            if 'path' in yaml:
                self.path = yaml['path']
            if 'key' in yaml:
                self.key = yaml['key']
            if 'ordinal' in yaml:
                self.ordinal = int(yaml['ordinal'])


class table_ownership:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.group = None
        self.entity = None
        self.location = None
        if None != yaml:
            if 'group' in yaml:
                self.group = yaml['group']
            if 'entity' in yaml:
                self.entity = yaml['entity']
            if 'location' in yaml:
                self.location = yaml['location']


class table_delimiters:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.field = ","
        self.array = "|"
        self.error = "#"
        self.block_quote = None
        self.comment = ["#", ";", "/"]
        # TODO hard coding this for a moment... must think
        self.new_line = "UNIX"
        if None != yaml:
            if 'field' in yaml:
                self.field = yaml['field']
            if 'error' in yaml:
                self.error = yaml['error']
            if 'array' in yaml:
                self.array = yaml['array']
            if 'comment' in yaml:
                self.comment = yaml['comment']
            if 'block_quote' in yaml:
                self.block_quote = yaml['block_quote']
                if isinstance(self.block_quote, str):
                    if not self.block_quote.strip():
                        self.block_quote = None
                else:
                    self.block_quote = None
