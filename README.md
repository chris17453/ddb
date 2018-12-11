# ddb
 A sql interface for flat files written in python 


## Prerequisites (Fedora)
- yum install -y redhat-rpm-config   # for cython deps
- yum install -y python2-devel       # for cython deps
- yum install -y libyaml-devel       # for c bindings on config loader

## Install
```
pip install ddb
# OR
pipenv install ddb
```

### Commandline interface
```
ddb
# OR
ddb --query 'select * from `tablename` where column=value limit 0,10'
```

### Code integration
```
import ddb

engine=ddb.engine(mode='object')

# defining the table.
# not needed if you define out of code in the cli app with "create table"
engine.define_table(table_name='test_table',database_name='test_Db',field_delimiter=',',
                            columns=['name','document','os','id','price','qty','value'],
                            data_file='/MOCK_DATA.csv')

# standard query
query="SELECT * FROM `test_table` WHERE id='{}'".format(id)

# an array of matched results
# None if an invalid query or error
# an empty array if nothing matches the query
results=self.engine.query(query)


```


### Query support
- Query support is limited. As needed I'll improve the system.
- If you're doing vastly comlicated things, it shouldn't be with a flat file.
- This code is not fast, but not slow either. It will be refactored, but not until more support is added.
- compiled with cpython gives a 450%+ boost in execution time. 
- My test record set with 60k records, at first, came back in 1.6 seconds, now comes in at .35 seconds


### Supported Querys
- USE [DATABASE]
- SHOW TABLES
- SHOW COLUMNS FROM [TABLE]
- CREATE TABLE [TABLE] ([COLUMNS]) file=[DATA_FILE_PATH]
- DROP TABLE [TABLE]
- SELECT [[COLUMN [AS COLUMN]]] FROM [TABLE] [WHERE] [AND] [OR] [ORDER BY] [LIMIT]
- INSERT INTO [TABLE] ([[COLUMNS]]) VALUES ([[VALUES])
- DELETE FROM [TABLE] [WHERE] [AND] [OR]
- UPDATE [TABLE] SET [[COLUMN=VALUE]] [WHERE]


### Not supported
- Right now this is a POC, complex operations are not supported, but are in the works.
- JOIN, COUNT, SUM, DISTINCT, GROUP BY are all high on the list

### TODO
- curses browser for results
- unit testing

### Examples

# SELECT
# UPDATE
# INSERT
# DELETE
# CONFIG
```
```

### Demo
![Demo](https://raw.githubusercontent.com/chris17453/ddb/master/data/ddb-demo.gif)


### Notes to self
- cython builds the python code as a ".so"
- packages can see down, not up
- in code import using full package name
- cython packages must be marked as extensions
- all pure cython packages must be marked as packages in setup, otherwise "le fail"
