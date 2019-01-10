## ddb Examples


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
