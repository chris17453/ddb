# cython: linetrace=True
import os
from .table import table
import warnings
import sys
from ..output.factory_yaml import yamlf_load, yamlf_dump
from ..file_io.locking import normalize_path


class database:
    tables = []

    def __init__(self, config_file=None):
        self.curent_database = None
        self.tables = []
        self.config_file = None
        is_file = False

        if None != config_file and config_file != False:
            self.config_file = config_file
            # loads the config in a safe way
            #self.reload_config()

    def set_database(self, database_name):
        # TODO validate database name
        self.curent_database = database_name

    def get(self, table_name, database_name=None):
        """Get a Table structure in the database."""
        if None == database_name:
            database_name = self.get_curent_database()
        #print("Matching  {0}".format(database_name))
        for c in self.tables:
          #  print("Using {0}.{1} matching {2}.{3}".format(c.data.database,c.data.name, database_name,table_name))
            if c.data.name == table_name and database_name == c.data.database:
                return c
        return None
        #raise Exception("Error: configs.get -> can't find configuration for table:{}".format(table_name))

    def count(self):
        """Return a count ot tables in the database"""
        return len(self.tables)

    def temp_table(self, name=None, columns=[], delimiter=None):
        """Create a temporary table to preform operations in"""
        if None == name:
            name = "#table_temp"  # TODO make unique random name
        return table(name=name, columns=columns, database=self.get_curent_database(), field_delimiter=delimiter)

    def create_config(self, config_file):
        try:
            if False == os.path.exists(config_file):
                dirname = os.path.dirname(config_file)
                if False == os.path.exists(dirname):
                    os.makedirs(dirname)
                #print ("Successfully created the directory %s " % path)
            yaml_data = {}
            #print ("Creating new db config")
            yamlf_dump(yaml_data, file=config_file)
            #print ("Created new db config")
            return
        except Exception as ex:
            print("Cant create configuration file: {0}".format(ex))

    def create_table_config(self, name, db, columns, delimiter=None):
        if None == self.config_file:
            raise Exception("Not using a config file")

        t = table(name=name, database=db, columns=columns,
                  field_delimiter=delimiter)
        t.save()
        self.add_config(t.data.path)

    def add_config(self, table_config=None, table=None):
        if None == self.config_file:
            raise Exception("Not using a config file")
        if not os.path.exists(self.config_file):
            self.create_config(self.config_file)

        # if we have a file name, lets add it
        if None != table_config:
            #print "Adding table config"
            # if the file doesnt exist. create it
            self.create_config(self.config_file)
            config = table(table_config)
            yaml_data = yamlf_load(file=self.config_file)
            db = config.data.database
            if None == db:
                db = self.get_default_database()

            if db not in yaml_data:
                yaml_data[db] = {}

            yaml_data[db][config.data.name] = {
                'name': config.data.name, 'path': table_config}
            yamlf_dump(yaml_data, file=self.config_file)

        # if we have a table lets save it
        if table is not None:
            yaml_data = yamlf_load(file=self.config_file)
            if None == yaml_data:
                yaml_data = {}
            db = table.data.database
            if None == db:
                db = self.get_default_database()

            if db not in yaml_data:
                yaml_data[db] = {}

            yaml_data[db][table.data.name] = {
                'name': table.data.name, 'path': table.data.config}
            yamlf_dump(yaml_data, file=self.config_file)
        return True

    def get_default_database(self):
        if self.curent_database is None:
            return 'main'

    def get_curent_database(self):
        if self.curent_database is None:
            return self.get_default_database()
        return self.curent_database

    def create_table(self, table_name, columns, data_file,
                     database_name=None,
                     delimiter=None,
                     comments=None,
                     errors=None,
                     whitespace=None,
                     data_on=None,
                     temporary=None,
                     fifo=None,
                     repo_type=None,
                     repo_url=None,
                     repo_user=None,
                     repo_password=None,
                     repo_dir=None,
                     repo_file=None,
                     strict_columns=None,
                     mode=None
                    ):
        print("Creating table..")
        if None == database_name:
            database_name = self.get_curent_database()
        exists = self.get(table_name, database_name)
        # it exists. so no dont create it
        if None != exists:
            raise Exception("table already exists")
        
        if repo_type!='svn':
            if False == os.path.isfile(normalize_path(data_file)):
                raise Exception("Data file does not exist")

        if not temporary:
            if None == self.config_file:
                raise Exception("Not using a config file")
            config_directory = os.path.dirname(self.config_file)
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
                    fifo=fifo,
                    repo_type=repo_type,
                    repo_url=repo_url,
                    repo_user=repo_user,
                    repo_password=repo_password,
                    repo_dir=repo_dir,
                    repo_file=repo_file,
                    strict_columns=strict_columns,
                    mode=mode)
        t.data.path = data_file
        # print("Appending table")
        self.tables.append(t)
        if not temporary:
            res = t.save()
            self.add_config(table=t)
            if False == res:
                raise Exception("Couldn't save table configuation")
            #self.add_config(table=t)
            #self.reload_config()
        return True

    def drop_table(self, table_name, database_name=None):
        #print("Database.drop table")
        if None == database_name:
            database_name = self.get_curent_database()
        #print table_name,database_name
        for index in range(0, len(self.tables)):
            #print( self.tables[index].data.name, table_name,self.tables[index].data.database,database_name)
            if self.tables[index].data.name == table_name and self.tables[index].data.database == database_name:
                #print("Found table")
                if self.tables[index].data.type=="Temp":
                    self.tables.pop(index)
                    #self.reload_config()
                    return True
                #print("Removing Table from config")
                res = self.remove_config(table_object=self.tables[index])
                if False == res:
                    raise Exception("Failed to remove configuration for table")
                self.tables.pop(index)
                #self.reload_config()
                return True
                break
        raise Exception("Failed to drop table. Does not exist")

    def remove_config(self, table_config=None, table_object=None):
        try:
            if not os.path.exists(self.config_file):
                self.create_config(self.config_file)
            if table_object is None:
                config = table(table_config)
            else:
                config = table_object
            yaml_data = yamlf_load(file=self.config_file)
            db = config.data.database
            if None == db:
                db = self.get_default_database()

            if db not in yaml_data:
                yaml_data[db] = {}

            table_name = config.data.name
            #print db,table_name
            if table_name in yaml_data[db]:
                yaml_data[db].pop(table_name, None)

            yamlf_dump(yaml_data, file=self.config_file)
            return True
        except Exception as ex:
            raise Exception("failed to remove table from db configuration")

    def get_db_sql(self):
        temp_tables = self.get_tables()
        queries=[]
        for t in temp_tables:
            with open(t,'r') as table_config:
                queries.append(table_config.read())
        return ";".join(queries)
            
    #def reload_config(self):
    #    temp_tables = self.get_tables()
    #    table_swap = []
    #    # add temp tables to list
    #    for t in self.tables:
    #        if t.data.type == 'Temp':
    #            table_swap.append(t)
    #
    #    for t in temp_tables:
    #        #temp_table = table(table_config_file=t)
    #        queries=""
    #        with open(t,'r') as table_config:
    #            queries.append(table_config.read())
    #        # Dont add tables that are inactive...
    #        #if temp_table.active == False:
    #        #    warn_msg="Table not loaded {0}.{1}".format(temp_table.data.database, temp_table.data.name)
    #        #    warnings.warn(message=warn_msg)
    #        #    continue
    #        #table_swap.append(temp_table)
    #
    #    self.tables = table_swap

    def get_tables(self):
        if None == self.config_file:
            return []

        if False == os.path.exists(self.config_file):
            return []

        tables = []

        #print("Loading config file: {0}".format(self.config_file))
        yaml_data = yamlf_load(file=self.config_file)
        # could be empty
        if yaml_data != None:
            for db in yaml_data:
                if yaml_data[db] != None:
                    #print("Loading database: {0}".format(db))
                    for table in yaml_data[db]:
                        #print("Loading table: {0},{1}".format(table,yaml_data[db][table]['path']))
                        tables.append(yaml_data[db][table]['path'])

        return tables
