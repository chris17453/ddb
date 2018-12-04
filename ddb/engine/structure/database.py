import os
import glob
import copy
from table import table
import yaml

class database:
    tables=[]
    def __init__(self,directory=None,config_file=None,show_config=False):
        self.tables=[]
        is_file=False

        if None !=config_file:
            self.config_file=config_file
            tables=self.get_tables()
            for table_file in tables:
                self.tables.append(table(table_file,show_config))
            return

        if isinstance(directory,list):
            for table_file in directory:
                if False == os.path.isdir(table_file):
                    if False == os.path.isfile(table_file):
                        raise Exception("Not a directory or a file: {}".format(table_file))
                self.tables.append(table(table_file,show_config))
            return
        else:
            self.config_file=None
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
    

    def create_config(self,config_file):
        try:
            if not os.path.exists(config_file):
                yaml_data={}
                f = open(config_file, "w")
                yaml.dump(yaml_data, f)
                f.close()
                return
        except Exception as ex:
            print ex    


    def create_table_config(self,name,db,columns):
        if None==self.config_file:
            raise Exception ("Not using a config file")
        t=table(name=name,database=db,columns=columns)
        t.save()
        self.add_config(t.data.path)


    def add_config(self,table_config):
        try:
            if None==self.config_file:
                raise Exception ("Not using a config file")
            if not os.path.exists(self.config_file):
                self.create_config(self.config_file)
        
            with open(self.config_file, 'r') as stream:
                config=table(table_config)
                yaml_data=yaml.load(stream)
                db=config.data.database
                if None == db:
                    db='main'
                
                if db not in  yaml_data:
                    yaml_data[db]={}

                yaml_data[db][config.data.name]={'name':config.data.name,'path':table_config}
                
                f = open(self.config_file, "w")
                yaml.dump(yaml_data, f)
                f.close()
        except Exception as ex:
                print ex    

    def create_table(self,database_name,table_name,columns,data_file):
        if None==self.config_file:
            raise Exception ("Not using a config file")
        t=table(name=table_name,database=database_name,columns=columns)
        t.data.path=data_file
        t.save()
        self.add_config(t.data.path)
    

    def drop_table(self,database_name,table_name):
        for index in range(0,len(self.tables)):
            if self.tables[index].data.name==table_name and tables[index].data==database_name:
                self.tables.remove(index)
                self.remove_config(self.tables[index].data.path)
                break



    def remove_config(self,table_config):
        try:
            if not os.path.exists(self.config_file):
                self.create_config(self.config_file)

            with open(self.config_file, 'r') as stream:
                config=table(table_config)
                yaml_data=yaml.load(stream)
                db=config.data.database
                if None == db:
                    db='Default'
                
                if db not in  yaml_data:
                    yaml_data[db]={}

                table_name=config.data.name
                #print db,table_name
                if table_name in yaml_data[db]:
                    yaml_data[db].pop(table_name, None)

                
                f = open(self.config_file, "w")
                yaml.dump(yaml_data, f)
                f.close()
        except Exception as ex:
                print ex    
            
    def get_tables(self):
        if not os.path.exists(self.config_file):
                self.create_config(self.config_file)
        tables=[]
        with open(self.config_file, 'r') as stream:
            yaml_data=yaml.load(stream)
            
            for db in  yaml_data:
                for table in yaml_data[db]:
                    tables.append(yaml_data[db][table]['path'])

        return tables

