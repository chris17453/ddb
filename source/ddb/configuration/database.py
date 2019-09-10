# cython: linetrace=True
import os
from .table import table
import warnings
import sys
from ..output.factory_yaml import yamlf_load, yamlf_dump
from ..file_io.locking import normalize_path


class database:
    tables = []

    def __init__(self, config_dir=None):
        self.tables = []
        self.curent_database = None
        self.config_dir=config_dir

    def count(self):
        """Return a count ot tables in the database"""
        return len(self.tables)

    def get_default_database(self):
        """Return default database"""
        if self.curent_database is None:
            return 'main'

    def get_curent_database(self):
        """Return current or default database"""
        if self.curent_database is None:
            return self.get_default_database()
        return self.curent_database

    def get(self, table_name, database_name=None):
        """Get a Table structure in the database."""
        if None == database_name:
            database_name = self.get_curent_database()
        for c in self.tables:
          #  print("Using {0}.{1} matching {2}.{3}".format(c.data.database,c.data.name, database_name,table_name))
            if c.data.name == table_name and database_name == c.data.database:
                return c
        return None

    def get_db_sql(self):
        """Return a string of table creation queries"""
        temp_tables = self.get_sql_definition_paths()
        queries=[]
        for sql_path in temp_tables:
            if False==os.path.exists(sql_path):
                raise Exception ("Path to table '{0}' is invalid".format(sql_path))
            with open(sql_path,'r') as table_config:
                queries.append(table_config.read())

        return ";\n".join(queries)

    def get_sql_definition_paths(self):
        """Return a list of paths to text files containing sql queries"""
        if None == self.config_dir:
            return []

        tables = []

        for file in os.listdir(self.config_dir):
            if file.endswith(".table.sql"):
                table_path=os.path.join(self.config_dir, file)
                tables.append(table_path)
        
        return tables


    def drop_table(self, table_name, database_name=None):
        """Remove a table configuration"""
        #print("Database.drop table")
        if None == database_name:
            database_name = self.get_curent_database()
        #print table_name,database_name
        for index in range(0, len(self.tables)):
            #print( self.tables[index].data.name, table_name,self.tables[index].data.database,database_name)
        
            target_table=self.tables[index]
            if target_table.data.name == table_name and target_table.data.database == database_name:
                #print("Found table")
                if target_table.data.type=="Temp":
                    self.tables.pop(index)
                    return True
                # deletes tabels by "/{config}/{db}.{table}.table.sql"
                target_table.delete()
                self.tables.pop(index)
                return True
                break

        raise Exception("Failed to drop table. Does not exist")


    def create_table(self, table_name, columns, data_file,
                     database_name=None,
                     delimiter=None,
                     comments=None,
                     errors=None,
                     whitespace=None,
                     data_on=None,
                     temporary=None,
                     fifo=None,
                     repo=None,
                     strict_columns=None,
                     mode=None
                    ):
        #print("Creating table..")
        if None == database_name:
            database_name = self.get_curent_database()
        exists = self.get(table_name, database_name)
        # it exists. so no dont create it
        if None != exists:
            raise Exception("table already exists")

        if repo:
            
            if repo.protocol!='svn':
                protocol_svn='svn'
                abs_data_file=normalize_path(data_file)
                if False == os.path.isfile(abs_data_file):
                    err="Data file does not exist. {0}".format(abs_data_file)
                    raise Exception(err)
            

        if not temporary:
            if None == self.config_dir:
                raise Exception("Not using a config file")

            config_directory = self.config_dir
        else:
            config_directory = None

        # print("Creating {0}.{1}".format(database_name,table_name))
        t = table(  name=table_name,
                    database=database_name,
                    columns=columns,
                    config_directory=config_directory,
                    field_delimiter=delimiter,
                    data_on=data_on,
                    comments=comments,
                    whitespace=whitespace,
                    errors=errors,
                    data_file=data_file,
                    fifo=fifo,
                    repo=repo,
                    strict_columns=strict_columns,
                    mode=mode)
        # print("Appending table")
        self.tables.append(t)
        if not temporary:
            res = t.save()
            if False == res:
                raise Exception("Couldn't save table configuation")
            #self.add_config(table=t)
            #self.reload_config()
        return True

    def temp_table(self, name=None, columns=[], delimiter=None):
        """Create a temporary table to preform operations in"""
        if None == name:
            name = "#table_temp"  # TODO make unique random name
        return table(name=name, columns=columns, database=self.get_curent_database(), field_delimiter=delimiter)

           