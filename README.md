# ddb (delimited database)

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
- uses python 2.7

## Install

```bash
pip install ddb
```

OR

```bash
pipenv install ddb
```

## Dev

- use the makefile
- make build.. etc


### Commandline interface

```bash
ddb
ddb 'select * from `tablename` where column=value limit 0,10'
ddb 'select * from `tablename` where column=value limit 0,10' --config=my_database_config_file.yaml
```

### Code integration

```python
import ddb

engine=ddb.engine(mode='object')

# defining the table.
# not needed if you define out of code in the cli app with "create table"
# you could even create the table with a query in code, and not use the class function
engine.define_table(table_name='test_table',
                    database_name='test_db',
                    field_delimiter=',',
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
- CREATE TABLE [TABLE] ([COLUMNS]) file=[DATA_FILE_PATH] delimiter=[FIELD_DELIMITER(default=',')] [WHITESPACE=bool] [ERRORS=bool] [COMMENTS=bool] data_on=[DATA_BEGINS_AT_LINE(default=1)] 
- DROP TABLE [TABLE]
- SELECT [[COLUMN [AS COLUMN]]|[FUNCTION(...) [AS COLUMN]]] FROM [TABLE] [WHERE] [AND] [OR] [ORDER BY] [LIMIT]
- INSERT INTO [TABLE] ([[COLUMNS]]) VALUES ([[VALUES])
- DELETE FROM [TABLE] [WHERE] [AND] [OR]
- UPDATE [TABLE] SET [[COLUMN=VALUE]] [WHERE]
- DESCRIBE TABLE [TABLE]
- UPDATE TABLE [TABLE] ([COLUMNS]) file=[DATA_FILE_PATH] delimiter=[FIELD_DELIMITER(default=',')] [WHITESPACE=bool] [ERRORS=bool] [COMMENTS=bool] data_on=[DATA_BEGINS_AT_LINE(default=1)] 

### Supported functions

- database()
- version()
- datetime()
- date()
- time()

### TODO

- curses browser for results (wil be built in flextable)
- output to yaml,json,raw, csv formatted string (should be simple)
- adding test cases for tokenizing
- aggregate function support 
- functions: COUNT, JOIN, SUM, DISTINCT, GROUP BY are all high on the list in that order

### Recent additions

- sql function: "version()" returns ddb version
- created output options json/yaml/raw/xml/term
- removed bumpversion
- updated pyyaml
- pyinstaller creates single file executable for packaging. in dist/
- makefile
- unittesting for basic operations
- base support for non aggregate functions in select column, with renaming, up to 3 parameters
- sql function: "database()" returns the curently selected database context
- added sql parsing support for join, left join, right join, full join *not implimented*
- added sql parsing support renaming tables "AS" with joins and from *not implimented*

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

Changes the database context, all operations after this apply to that context

```
USE main
┌┤changed_db                                                                              ├┐
│main                                                                                      │
└[changed_db                                                                              ]┘

```

### CREATE TABLE

creates a table in a database. If no context is used, the default context of 'main' is used.

```sql
USE test;
create table test('id','first_name','last_name','email','gender','ip_address') file='/test/MOCK_DATA.csv'
┌┤create table                                                                            ├┐
│1                                                                                         │
└[create table                                                                            ]┘
```

### DROP TABLE

removes a table from the database. It does not alter the data_file or the table configuration file.

```sql
USE test;
drop table test
┌┤dropped                                                                                 ├┐
│1                                                                                         │
└[dropped                                                                                 ]┘
```

### SHOW TABLES
list all tables in the system. ? maybe by database. But I think its all of them. #TODO FIX

```sql
show tables
┌┤database                                     ├┬┤table                                   ├┐
│main                                           │test                                      │
└[database                                     ]┴[table                                   ]┘
```

### SHOW COLUMNS FROM TABLE
list all of the columns of a given table

```sql
USE test;
show columns from test
┌┤table                                        ├┬┤column                                 ├┐
│test                                           │id                                       │
│test                                           │first_name                               │
│test                                           │last_name                                │
│test                                           │email                                    │
│test                                           │gender                                   │
│test                                           │ip_address                               │
└[table                                        ]┴[column                                 ]┘
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

```sql
USE test;
SELECT database()
SELECT * FROM TEST LIMIT 10
SELECT * from test limit 5,10
SELECT id,first_name from test order by id limit 15,10
SELECT *,id AS ID2,database() AS db_name FROM test WHERE id >990 AND gender LIKE 'Ma%' or id=1  ORDER BY gender,id desc LIMIT 0,1000
┌┤id  ├┬┤first_nam├┬┤last_name├┬┤email    ├┬┤gender   ├┬┤ip_addres├┬┤ID2    ├┬┤db_name   ├┐
│999   │Karlik     │Terrett    │kterrettrq@│Male       │55.93.204.4│999      │main        │
│998   │Calvin     │Hedger     │chedgerrp@g│Male       │171.110.129│998      │main        │
│995   │Peter      │Oliff      │poliffrm@si│Male       │104.255.33.│995      │main        │
│994   │Valentijn  │Dentith    │vdentithrl@│Male       │171.49.46.7│994      │main        │
│992   │Bernarr    │Playle     │bplaylerj@s│Male       │201.5.16.21│992      │main        │
│991   │Waite      │Pettipher  │wpettipherr│Male       │236.2.105.1│991      │main        │
│1     │Say        │Murgatroyd │smurgatroyd│Male       │35.226.127.│1        │main        │
└[id  ]┴[first_nam]┴[last_name]┴[email    ]┴[gender   ]┴[ip_addres]┴[ID2    ]┴[db_name   ]┘

```

### UPDATE

update a row in the database based on a standard where clause.
If no data is matched in the where, nothing is updated

```sql
USE test;
UPDATE 'test' SET first_name='TEST_UPDATE' where id='1001' or id='1001'
┌┤updated                                                                                ├┐
│0                                                                                        │
└[updated                                                                                ]┘
```

### INSERT

insert a row of data into the database, columns can be orderd

```sql
USE test;
INSERT INTO test (id,first_name,last_name,email,gender,ip_address) values (10001,test_name1,'test_lname','sam@bob.com','male','0.0.0.0');
INSERT INTO test (ip_address,id,first_name,last_name,email,gender) values ('0.0.0.0',10002,test_name1,'test_lname','sam@bob.com','male');
INSERT INTO test (id,first_name,last_name,email,gender,ip_address) values (10003,test_name1,'test_lname','sam@bob.com','male','0.0.0.0');
┌┤inserted                                                                               ├┐
│1                                                                                        │
└[inserted                                                                               ]┘
```

## DELETE

remove a row from the database based on matching criteria

```sql
USE test;
DELETE FROM test where email like 'sam%'
┌┤deleted                                                                                ├┐
│0                                                                                        │
└[deleted                                                                                ]┘
```

### DESCRIBE TABLE
-view table configuration
```sql
use test;
describe table test
┌┤option                                ├┬┤value                                         ├┐
│active                                  │True                                            │
│table_name                              │test                                            │
│database                                │main                                            │
│data_file                               │ddb/test/MOCK_DATA.csv                          │
│type                                    │Temp                                            │
│config_file                             │                                                │
│data_starts_on                          │0                                               │
│field_delimiter                         │,                                               │
│comments_visible                        │False                                           │
│errors_visible                          │True                                            │
│whitespace_visible                      │False                                           │
└[option                                ]┴[value                                         ]┘
```

### UPDATE TABLE
Change the properties of a table
```
update table test whitespace=true
┌┤update table                                                                           ├┐
│1                                                                                        │
└[update table                                                                           ]┘
```

### Docker

- TODO


### Walkthrough

```sql
[test]$ddb

Welcome! Type ? to list commands
ddb> use test_db
┌┤changed_db                                                                             ├┐
│test_db                                                                                  │
└[changed_db                                                                             ]┘
>>> executed in 0.00117802619934 seconds 

ddb> create table mock (id,first_name,last_name,email,gender,ip_address) file='ddb/test/MOCK_DATA.csv' delimiters=','
┌┤create table                                                                           ├┐
│1                                                                                        │
└[create table                                                                           ]┘
>>> executed in 0.225665092468 seconds 

ddb> show tables
┌┤database                                   ├┬┤table                                    ├┐
│main                                         │test                                       │
│test_db                                      │mock                                       │
└[database                                   ]┴[table                                    ]┘
>>> executed in 0.00108098983765 seconds 

ddb> show columns from mock
┌┤table                                      ├┬┤column                                   ├┐
│mock                                         │id                                         │
│mock                                         │first_name                                 │
│mock                                         │last_name                                  │
│mock                                         │email                                      │
│mock                                         │gender                                     │
│mock                                         │ip_address                                 │
└[table                                      ]┴[column                                   ]┘
>>> executed in 0.00223302841187 seconds 

ddb> select * from mock limit 10
select * from mock limit 10
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│id            │first_name    │last_name     │email         │gender        │ip_address    │
│1             │Say           │Murgatroyd    │smurgatroyd0@u│Male          │35.226.127.123│
│2             │Redford       │Ornils        │rornils1@amazo│Male          │24.42.186.82  │
│3             │Grenville     │Buckley       │gbuckley2@gizm│Male          │143.223.126.20│
│4             │Thalia        │Badrock       │tbadrock3@xinh│Female        │113.57.179.78 │
│5             │Julie         │Minchell      │jminchell4@sky│Female        │105.165.149.12│
│6             │Lancelot      │Archibold     │larchibold5@pi│Male          │213.155.189.44│
│7             │Bernie        │Matteucci     │bmatteucci6@br│Male          │109.156.49.36 │
│8             │Flinn         │Mulchrone     │fmulchrone7@na│Male          │22.84.116.46  │
│9             │Seamus        │Tocque        │stocque8@cnet.│Male          │79.30.35.75   │
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00982999801636 seconds 

ddb> update mock set id=1001 where id=1
┌┤updated                                                                                ├┐
│1                                                                                        │
└[updated                                                                                ]┘
>>> executed in 0.00821018218994 seconds 

ddb> select * from mock where id=1001
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│1001          │Say           │Murgatroyd    │smurgatroyd0@u│Male          │35.226.127.123│
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.0078330039978 seconds 

ddb> delete from mock where id=1001
┌┤deleted                                                                                ├┐
│1                                                                                        │
└[deleted                                                                                ]┘
>>> executed in 0.00804209709167 seconds 

ddb> select * from mock where id=1001
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00705003738403 seconds 

ddb> insert into  mock (id,first_name,last_name,email,gender,ip_address) values(1,n1,n2,'sam#sam.com',Male,'0.0.0.0')
┌┤inserted                                                                               ├┐
│1                                                                                        │
└[inserted                                                                               ]┘
>>> executed in 0.015517950058 seconds 

ddb> select * from mock where id=1
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│1             │n1            │n2            │sam#sam.com   │Male          │0.0.0.0       │
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00686001777649 seconds 

ddb> select * from mock limit 10
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│id            │first_name    │last_name     │email         │gender        │ip_address    │
│2             │Redford       │Ornils        │rornils1@amazo│Male          │24.42.186.82  │
│3             │Grenville     │Buckley       │gbuckley2@gizm│Male          │143.223.126.20│
│4             │Thalia        │Badrock       │tbadrock3@xinh│Female        │113.57.179.78 │
│5             │Julie         │Minchell      │jminchell4@sky│Female        │105.165.149.12│
│6             │Lancelot      │Archibold     │larchibold5@pi│Male          │213.155.189.44│
│7             │Bernie        │Matteucci     │bmatteucci6@br│Male          │109.156.49.36 │
│8             │Flinn         │Mulchrone     │fmulchrone7@na│Male          │22.84.116.46  │
│9             │Seamus        │Tocque        │stocque8@cnet.│Male          │79.30.35.75   │
│10            │Lazare        │Abbett        │labbett9@who.i│Male          │17.173.76.145 │
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00780391693115 seconds 

ddb> select * from mock order by id limit 10
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│1             │n1            │n2            │sam#sam.com   │Male          │0.0.0.0       │
│10            │Lazare        │Abbett        │labbett9@who.i│Male          │17.173.76.145 │
│100           │Eleanor       │Heditch       │eheditch2r@ocn│Female        │124.231.187.47│
│1000          │Curcio        │Kemm          │ckemmrr@irs.go│Male          │14.143.73.253 │
│10003         │test_name1    │test_lname    │sam@bob.com   │male          │0.0.0.0       │
│101           │Curry         │Kerkham       │ckerkham2s@app│Male          │139.216.9.172 │
│102           │Joanna        │Simone        │jsimone2t@dion│Female        │48.225.191.89 │
│103           │Giffie        │Aikin         │gaikin2u@noaa.│Male          │9.169.172.177 │
│104           │Rosalinda     │Hedin         │rhedin2v@aol.c│Female        │239.132.244.29│
│105           │Jolyn         │Smy           │jsmy2w@deviant│Female        │220.24.157.8  │
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00986289978027 seconds 

```

## CLI Output examples
You can specify the output type
- bash (bash style variables)
- term (human readable)
- xml 
- yaml 
- json

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o raw
3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204
1,n1,n2,sam#sam.com,Male,0.0.0.0
```

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o xml
<?xml version="1.0" encoding="utf-8"?><data><results><raw><![CDATA[3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204]]></raw><type><![CDATA[3]]></type><data><![CDATA[3]]></data><data><![CDATA[Grenville]]></data><data><![CDATA[Buckley]]></data><data><![CDATA[gbuckley2@gizmodo.com]]></data><data><![CDATA[Male]]></data><data><![CDATA[143.223.126.204]]></data><error><![CDATA[]]></error></results><results><raw><![CDATA[1,n1,n2,sam#sam.com,Male,0.0.0.0]]></raw><type><![CDATA[3]]></type><data><![CDATA[1]]></data><data><![CDATA[n1]]></data><data><![CDATA[n2]]></data><data><![CDATA[sam#sam.com]]></data><data><![CDATA[Male]]></data><data><![CDATA[0.0.0.0]]></data><error><![CDATA[]]></error></results><columns><![CDATA[id]]></columns><columns><![CDATA[first_name]]></columns><columns><![CDATA[last_name]]></columns><columns><![CDATA[email]]></columns><columns><![CDATA[gender]]></columns><columns><![CDATA[ip_address]]></columns></data>
```

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o json
{"results": [{"raw": "3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204", "type": 3, "data": ["3", "Grenville", "Buckley", "gbuckley2@gizmodo.com", "Male", "143.223.126.204"], "error": null}, {"raw": "1,n1,n2,sam#sam.com,Male,0.0.0.0", "type": 3, "data": ["1", "n1", "n2", "sam#sam.com", "Male", "0.0.0.0"], "error": null}], "columns": ["id", "first_name", "last_name", "email", "gender", "ip_address"]}
```

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o yaml
columns:
- id
- first_name
- last_name
- email
- gender
- ip_address
results:
- data:
  - '3'
  - Grenville
  - Buckley
  - gbuckley2@gizmodo.com
  - Male
  - 143.223.126.204
  error: null
  raw: 3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204
  type: 3
- data:
  - '1'
  - n1
  - n2
  - sam#sam.com
  - Male
  - 0.0.0.0
  error: null
  raw: 1,n1,n2,sam#sam.com,Male,0.0.0.0
  type: 3
  ```

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o term
┌┤id                  ├┬┤first_name          ├┬┤last_name           ├┬┤email               ├┬┤gender              ├┬┤ip_address          ├┐
│3                     │Grenville             │Buckley               │gbuckley2@gizmodo.com │Male                  │143.223.126.204       │
│1                     │n1                    │n2                    │sam#sam.com           │Male                  │0.0.0.0               │
└[id                  ]┴[first_name          ]┴[last_name           ]┴[email               ]┴[gender              ]┴[ip_address          ]┘
```

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o bash
# bash variable assignment for ddb output
declare ddb_data -A
declare ddb_info -A
declare ddb_columns -A

ddb_columns[0]='id'
ddb_columns[1]='first_name'
ddb_columns[2]='last_name'
ddb_columns[3]='email'
ddb_columns[4]='gender'
ddb_columns[5]='ip_address'
ddb_info[0,error]=''
ddb_info[0,type]='3'
ddb_info[0,raw]='3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204'
ddb_data[0,0]='3'
ddb_data[0,1]='Grenville'
ddb_data[0,2]='Buckley'
ddb_data[0,3]='gbuckley2@gizmodo.com'
ddb_data[0,4]='Male'
ddb_data[0,5]='143.223.126.204'
ddb_info[1,error]=''
ddb_info[1,type]='3'
ddb_info[1,raw]='1,n1,n2,sam#sam.com,Male,0.0.0.0'
ddb_data[1,0]='1'
ddb_data[1,1]='n1'
ddb_data[1,2]='n2'
ddb_data[1,3]='sam#sam.com'
ddb_data[1,4]='Male'
ddb_data[1,5]='0.0.0.0'
# end ddb output 
```


### Demo
![Demo](https://raw.githubusercontent.com/chris17453/ddb/master/data/ddb-demo.gif)

### Notes to self

- cython builds the python code as a ".so"
- packages can see down, not up
- in code import using full package name
- cython packages must be marked as extensions
- all pure cython packages must be marked as packages in setup, otherwise "le fail"