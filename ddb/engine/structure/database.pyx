import os
import glob
import copy
from .table import table
import yaml

class database:
    tables=[]
    def __init__(self,directory=None,config_file=None,show_config=False):
        self.curent_database=None
        self.tables=[]
        is_file=False
        self.config_file=None
        if None !=config_file and config_file!=False:
            self.config_file=config_file
            tables=self.get_tables()
            for table_file in tables:
                self.tables.append(table(table_file,show_config))
            return

        if None !=directory:
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
    
    def set_database(self,database_name):
        # TODO validate database name
        self.curent_database=database_name

    def get(self,table_name,database_name=None):
        """Get a Table structure in the database."""
        if None==database_name:
            database_name=self.get_curent_database()
        for c in self.tables:
            if c.data.name==table_name and database_name==c.data.database:
                return c
        return None
        #raise Exception("Error: configs.get -> can't find configuration for table:{}".format(table_name))
    
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
        return table(name=name,columns=columns,database=self.get_curent_database())
    

    def create_config(self,config_file):
        try:
            if False == os.path.exists(config_file):
                dirname=os.path.dirname(config_file)
                if False==os.path.exists(dirname):
                    os.makedirs(dirname)
                #print ("Successfully created the directory %s " % path)                
            yaml_data={}
            f = open(config_file, "w")
            yaml.dump(yaml_data, f)
            f.close()
            return
        except Exception as ex:
            print "Cant create configuration file: {}".format(ex)


    def create_table_config(self,name,db,columns):
        if None==self.config_file:
            raise Exception ("Not using a config file")
        t=table(name=name,database=db,columns=columns)
        t.save()
        self.add_config(t.data.path)


    def add_config(self,table_config=None,table=None):
        if None==self.config_file:
            raise Exception ("Not using a config file")
        if not os.path.exists(self.config_file):
            self.create_config(self.config_file)
        
        #if we have a file name, lets add it
        if None != table_config:
            print "Adding table config"
            with open(self.config_file, 'r') as stream:
                config=table(table_config)
                yaml_data=yaml.load(stream)
                db=config.data.database
                if None == db:
                    db=self.get_default_database()
                
                if db not in  yaml_data:
                    yaml_data[db]={}

                yaml_data[db][config.data.name]={'name':config.data.name,'path':table_config}
                
                f = open(self.config_file, "w")
                yaml.dump(yaml_data, f)
                f.close()



        #if we have a table lets save it
        if table !=None:
            with open(self.config_file, 'r') as stream:
                yaml_data=yaml.load(stream)
                db=table.data.database
                if None == db:
                    db=self.get_default_database()
                
                if db not in  yaml_data:
                    yaml_data[db]={}
                
                yaml_data[db][table.data.name]={'name':table.data.name,'path':table.data.config}
                f = open(self.config_file, "w")
                yaml.dump(yaml_data, f)
                f.close()
        return True


    def get_default_database(self):
        if self.curent_database==None:
            return 'main'


    def get_curent_database(self):
        if self.curent_database==None:
            return self.get_default_database()
        return self.curent_database


    def create_table(self,table_name,columns,data_file,database_name=None):
        if None==self.config_file:
            raise Exception ("Not using a config file")
        if False==os.path.isfile(data_file):
            raise Exception ("Data file does not exist")
        
        
        if None ==database_name:
            database_name=self.get_curent_database()
        exists=self.get(table_name,database_name)
        #it exists. so no dont create it
        if None!=exists:
            raise Exception("table already exists")

        t=table(name=table_name,database=database_name,columns=columns)
        t.data.path=data_file
        res=t.save()
        if False==res:
            raise Exception("Couldn't save table configuation")
        self.add_config(table=t)
        return True

    

    def drop_table(self,table_name,database_name=None):
        if None ==database_name:
            database_name=self.get_curent_database()
        #print table_name,database_name
        for index in range(0,len(self.tables)):
            #print self.tables[index].data.name,self.tables[index].data.database
            if self.tables[index].data.name==table_name and self.tables[index].data.database==database_name:
                res=self.remove_config(table_object=self.tables[index])
                if False==res:
                    return False
                self.tables.pop(index)
                return True
                break
        return False


    def remove_config(self,table_config=None,table_object=None):
        try:
            if not os.path.exists(self.config_file):
                self.create_config(self.config_file)
            with open(self.config_file, 'r') as stream:
                if table_object==None:
                    config=table(table_config)
                else:
                    config=table_object
                yaml_data=yaml.load(stream)
                db=config.data.database
                if None == db:
                    db=self.get_default_database()
                
                if db not in  yaml_data:
                    yaml_data[db]={}

                table_name=config.data.name
                #print db,table_name
                if table_name in yaml_data[db]:
                    yaml_data[db].pop(table_name, None)

                
                f = open(self.config_file, "w")
                yaml.dump(yaml_data, f)
                f.close()
                return True
        except Exception as ex:
                print ex   
                return False 


    def reload_config(self):
        temp_tables=self.get_tables()
        table_swap=[]
        # add temp tables to list
        for t in self.tables:
            if t.data.type=='Temp':
                table_swap.append(t)
                
        for t in temp_tables:
            self.tables.append(table(t))
        
        self.tables=table_swap
            
    def get_tables(self):
        if None==self.config_file: 
            return []

        if False==os.path.exists(self.config_file):
                self.create_config(self.config_file)
        
        tables=[]
        if False==os.path.exists(self.config_file):
            return []

        with open(self.config_file, 'r') as stream:
            yaml_data=yaml.load(stream)
            # could be empty
            if None !=yaml_data:
                for db in  yaml_data:
                    for table in yaml_data[db]:
                        tables.append(yaml_data[db][table]['path'])

        return tables

