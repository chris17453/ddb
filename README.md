# ddb

 A serviceless sql interface for flat files written in python.
 
## use 

- programatic access via python
- cli access

## usecase

- running queries on exported data
- automation of flat file data
- managing legacy flat files



## Prerequisites (Fedora)

- yum install -y python2-devel       # for cython deps
- yum install -y redhat-rpm-config   # for cython deps
- yum install -y libyaml-devel       # for c bindings on yaml reader 

## Install

```
pip install ddb
```
OR
```
pipenv install ddb
```

## Dev

- use the makefile
- make build.. etc


### Commandline interface

```
ddb
ddb 'select * from `tablename` where column=value limit 0,10'
ddb 'select * from `tablename` where column=value limit 0,10' --config=my_database_config_file.yaml
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
- This code is no t fast, but not slow either. It will be refactored, but not until more support is added.
- compiled with cython gives a 450%+ boost in execution time. 
- My test record set with 60k records, at first, came back in 1.6 seconds, now comes in at .35 seconds

### Supported Querys

- USE [DATABASE]
- SHOW TABLES
- SHOW COLUMNS FROM [TABLE]
- CREATE TABLE [TABLE] ([COLUMNS]) file=[DATA_FILE_PATH]
- DROP TABLE [TABLE]
- SELECT [[COLUMN [AS COLUMN]]|[FUNCTION(...) [AS COLUMN]]] FROM [TABLE] [WHERE] [AND] [OR] [ORDER BY] [LIMIT]
- INSERT INTO [TABLE] ([[COLUMNS]]) VALUES ([[VALUES])
- DELETE FROM [TABLE] [WHERE] [AND] [OR]
- UPDATE [TABLE] SET [[COLUMN=VALUE]] [WHERE]

### Supported functions

- database()

### TODO

- curses browser for results (wil be built in flextable)
- output to yaml,json,raw, csv formatted string (should be simple)
- adding test cases for tokenizing
- aggregate function support 
- functions: COUNT, JOIN, SUM, DISTINCT, GROUP BY are all high on the list in that order

### Recent additions

- unittesting has began!
- base support for non aggregate functions in select column, with renaming, up to 3 paramaters
- sql function: "database()" returns the curently selected database context

## Examples

- unless specified, all configurations apply to ~/.ddb/ddb.conf in your home directory
- this is a lookup file for the tables
- table configs are stored in a sub directory based on the db name
- ; is a command seperator. everything after this is a new command
- results are only returned for the last operation preformed
- all interactions are parsed directly from the data_files at time of execution
- 5 querys will consist of 5 file reads.
- anything inside of a block quote is treated as a single expression. '...' or "..." or [...]

### USE

- Changes the database context, all operations after this apply to that context
```
USE main
```

### CREATE TABLE

- creates a table in a database. If no context is used, the default context of 'main' is used.
```
USE test;
create table test('id','first_name','last_name','email','gender','ip_address') file='/test/MOCK_DATA.csv'
```

### DROP TABLE

- removes a table from the database. It does not alter the data_file or the table configuration file.
```
USE test;
drop table test
```

### SHOW TABLES

- list all tables in the system. ? maybe by database. But I think its all of them. #TODO FIX
```
show tables
```

### SHOW COLUMNS FROM TABLE

- list all of the columns of a given table

```
USE test;
show columns from test
```

### SELECT

- bring data back from the database
- nested querys are not supported
- "as like, not, is, or, and, where, from, order by,limit" are supported
- like '%x%' or like '%x' or like 'x%' 
- operators are supported. Though casting isnt setup yet
- =, >, >=, <, <=, like, not, is
- selecting from columns in a table requires a from target 
- selecting from functions does not require a table, they are calculated
- if a function is present and no table data is present, no data will be returned
- if a function is present and no columns are present, a single row will be returned

```
USE test;
SELECT database()
SELECT * FROM TEST LIMIT 10
SELECT * from test limit 5,10
SELECT id,first_name from test order by id limit 15,10
SELECT *,id AS ID2,database() AS db_name FROM test WHERE id >990 AND gender LIKE 'Ma%' or id=1  ORDER BY gender,id desc LIMIT 0,1000
```

### UPDATE

- update a row in the database based on a standard where clause
- If no data is matched in the where, nothing is updated

```
USE test;
UPDATE 'test' SET first_name='TEST_UPDATE' where id='1001' or id='1001'
```

### INSERT

- insert a row of data into the database, columns can be orderd

```
USE test;
INSERT INTO test (id,first_name,last_name,email,gender,ip_address) values (10001,test_name1,'test_lname','sam@bob.com','male','0.0.0.0');
INSERT INTO test (ip_address,id,first_name,last_name,email,gender) values ('0.0.0.0',10002,test_name1,'test_lname','sam@bob.com','male');
INSERT INTO test (id,first_name,last_name,email,gender,ip_address) values (10003,test_name1,'test_lname','sam@bob.com','male','0.0.0.0');
```

## DELETE

- remove a row from the database based on matching criteria

```
USE test;
DELETE FROM test where email like 'sam%'
```

### Demo
![Demo](https://raw.githubusercontent.com/chris17453/ddb/master/data/ddb-demo.gif)


### Notes to self
- cython builds the python code as a ".so"
- packages can see down, not up
- in code import using full package name
- cython packages must be marked as extensions
- all pure cython packages must be marked as packages in setup, otherwise "le fail"
