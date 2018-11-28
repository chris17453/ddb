import os
import glob
import copy
from table import table

class database:
    tables=[]
    def __init__(self,directory='.',show_config=False):
        self.tables=[]
        is_file=False

        if False == os.path.isdir(directory):
            if False == os.path.isfile(directory):
                raise Exception("Not a directory or a file: {}".format(directory))
            else:
                is_file=True

        if True == is_file:
            files=glob.glob(directory)
        else:
            files=glob.glob(directory+'/'+'*.ddb.yaml')

        if 0 == len(files):
            raise Exception("No configuration files in this directory : {}".format(directory))
        for cf in files:
            self.tables.append(table(cf,show_config))
        

    def get(self,table_name):
        """Get a Table structure in the database."""
        for c in self.tables:
            if c.data.name==table_name:
                return c
        raise Exception("Error: configs.get -> can't find configuration for table:{}".format(table_name))
    
    def count(self):
        """Return a count ot tables in the database"""
        return len(self.tables)
        
    def get_clone(self,table_name):
        """Clone a Table structure in the database."""
        table=self.get(table_name)
        if None == table:
            raise Exception("Table does not exist.{}".format(table_name))
        temp_table=copy.deepcopy(table)
        temp_table.columns=[]
        return temp_table

    def temp_table(self,name=None,columns=[]):
        """Create a temporary table to preform operations in"""
        if None==name:
            name="#table_temp" #TODO make unique random name
        return table(name=name,columns=columns)
        