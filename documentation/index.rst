========================
ddb 1.1 Reference Manual 
========================

ddb
***

:Author: Charles Watkins
:Version: $Revision: 1.1 $
:Copyright: This document has been placed in the public domain.


.. toctree::
   :maxdepth: 2
   :caption: Contents:


#.. contents::


Data Types
==========

CHAR
----
A singfle character of any ascii value

STRING
------
An unlimited collection of ascii characters.

INT
---
A python integer

FLOAT
------
A python float 

DECIMAL
-------
A python decimal

GUID
----
A 128 bit unique identifyer

Example:
    
 69121893-3AFC-4F92-85F3-40BB5E7C7E29	
   
IP
--
An IPV4 Address

Example:
 10.10.0.255


Functions and Operators
=======================
SUM
---
 FUTURE IMPLIMENTATION

COUNT
-----
 FUTURE IMPLIMENTATION

DATABASE
--------
The database function returns the curent database context.
The default context is main.

Example:
 SELECT DATABASE()

Results:
 
 +-----------------------------+
 | database                    |
 +=============================+
 | main                        |
 +-----------------------------+

DATE
----
Example:
 SELECT DATE()

Results:
 
 +-----------------------------+
 | date                        |
 +=============================+
 | 2019-03-12                  |
 +-----------------------------+

TIME
----
 SELECT TIME()
 
Results:
 
 +-----------------------------+
 | time                        |
 +=============================+
 | 19:58:44                    |
 +-----------------------------+


DATETIME
--------
Returns a python formatted datetime
 
Example:
 SELECT DATETIME()
 
Results:
 
 +-----------------------------+
 | datetime                    |
 +=============================+
 | 2019-03-12 19:48:55.849826  |
 +-----------------------------+

VERSION
-------
Version returns the **major** . **minor** . **patch** version of ddb.

Example:
 SELECT VERSION()
 
Results:

  +-----------------+
  | version         |
  +=================+
  | 1.1.118         |
  +-----------------+

Sql Syntaxt
===========
Data Defintion Statements
-------------------------
CREATE
``````


Configuration
Processing the file path
If the path starts with "~/" , the path is saved as is, and computed pre load.
If the path is relative, the absolute path is computed and saved.
If the path is absolute, it is saved as is.
If a file does exist at a given path, an error is raised.

Reasoning:
To support command line portability, paths within a users alias directory should
work if moved. This supports a healthy ci/cd and unitesting mindest. 
Deployment without reconfiguration. 


DROP
````
Syntax:
DROP [{DB}.]{Table}

Example:
DROP mock.table

Results:
Success or Failure

UPDATE
``````
@TRUNCATE TABLE
```````````````
Data Manipulation Statements 
----------------------------
SELECT
``````
Return data from the datbase. With the options of filtering and sorting.

Syntax:
read data from a table
- select_expr = { {column | function () } [AS display_name]}
- order_expression = { ASC | DESC }
SELECT [DISTINCT] select_expr [,select_expr ... ]
[FROM table
 [WHERE condition 
     [
         [AND condition] 
         [OR condition]
     ] 
 ]
 [ORDER BY {column_name} order_expression [,{column_name} order_expression ...]] 
]
[LIMIT [{offset, }] row_count]

Example:
SELECT date(),first_name,last_name,gender,ip as addr 
FROM beta.mock 
WHERE gender='Female' 
AND first_name like 'M%' 
AND last_name like 'M%' 
ORDER BY first_name 
LIMIT 5


Results:
+-----------+-----------+------------+--------+----------------+
|date       |first_name |last_name   |gender  |addr            |
+===========+===========+============+========+================+
|2019-03-20 |Mommy      |Mays        |Female  |240.245.233.199 |
+-----------+-----------+------------+--------+----------------+
|2019-03-20 |Millie     |Marjanski   |Female  |28.4.112.23     |
+-----------+-----------+------------+--------+----------------+
|2019-03-20 |Mellisent  |Meers       |Female  |61.179.170.24   |
+-----------+-----------+------------+--------+----------------+
|2019-03-20 |Melly      |Mickleburgh |Female  |235.116.155.238 |
+-----------+-----------+------------+--------+----------------+
|2019-03-20 |Marlo      |McCoveney   |Female  |95.32.37.87     |
+-----------+-----------+------------+--------+----------------+

executed in 0.017521, 5 rows returned


INSERT
``````
DELETE
``````
UPDATE
``````
Transactional Statements
------------------------
BEGIN
`````

COMMIT
``````

ROLLBACK
````````

Prepaired SQL Statement Syntaxt
-------------------------------
PREPARE
````````
FUTURE IMPLIMENTATION

EXECUTE
````````
FUTURE IMPLIMENTATION

Database Administration Statements
----------------------------------
SET
```
Sets a system or user variable. User variables are preappended with an '@'.
User variables can be used in prepared SQL statements.
If the system variable is invalid, an error is raised.

Syntax:
SET {variable}={value}

Example:
 SET @what=1,OUTPUT_MODULE=TERM;

 Results:
  Success or Failure

SHOW DATABASES
``````````````
Display the available database contexts available.

Syntax:
SHOW DATABASES

Example:
SHOW DATABASES

Results:


SHOW COLUMNS
````````````
Display the columns of a given table in the database.

Syntax:
SHOW COLUMNS FROM [{DB}.]{NAME}

Example:
ddb 'show columns from beta.mock'

Results:
+---------+-------+-----------+
|database |table  |column     |
+=========+=======+===========+
|beta     |mock   |id         |
+---------+-------+-----------+
|beta     |mock   |first_name |
+---------+-------+-----------+
|beta     |mock   |last_name  |
+---------+-------+-----------+
|beta     |mock   |email      |
+---------+-------+-----------+
|beta     |mock   |gender     |
+---------+-------+-----------+
|beta     |mock   |ip_address |
+---------+-------+-----------+

executed in 0.000093, 6 rows returned

SHOW TABLES
```````````
Display all of the availble tables in all databases.

Example:

+-----------+--------+
| database  | table  |
+===========+========+
| main      | test   |
+----------+---------+


SHOW VARIABLES
``````````````
Display all system and user variables.

Example:
 SHOW VARIABLES()

Results:
 +-------+--------------+------+
 |type   |name          |value |
 +=======+==============+======+
 |system |AUTOCOMMIT    |True  |
 +-------+--------------+------+
 |system |OUTPUT_MODULE |TERM  |
 +-------+--------------+------+
 |system |OUTPUT_STYLE  |RST   |
 +-------+--------------+------+
 |user   |WHAT          |1     |
 +-------+--------------+------+


Utility Statements
------------------
USE 
```
Change the curent database context. The default is main.

Example:
 USE test;

Results:
 Querys executed without a specified database will execute against this 
 database context.


EXPLAIN (QUERY)
```````````````
FUTURE IMPLIMENTATION

DESCRIBE 
````````
Display the configuration of a table in a database.

Example:
 DESCRIBE table test

Results:

+--------------------+----------------------------+
|option              |value                       |
+====================+============================+
|active              |True                        |
+--------------------+----------------------------+
|table_name          |mock                        |
+--------------------+----------------------------+
|database            |test                        |
+--------------------+----------------------------+
|data_file           |source/test/MOCK_DATA.csv   |
+--------------------+----------------------------+
|type                |Temp                        |
+--------------------+----------------------------+
|config_file         |                            |
+--------------------+----------------------------+
|data_starts_on      |0                           |
+--------------------+----------------------------+
|field_delimiter     |,                           |
+--------------------+----------------------------+
|comments_visible    |False                       |
+--------------------+----------------------------+
|errors_visible      |True                        |
+--------------------+----------------------------+
|whitespace_visible  |False                       |
+--------------------+----------------------------+


Errors, Error Codes
SQL Errors

Integration
bash
python
Syntax:
import ddb

 ddb(config_file=None,debug=False)
 
 Config file: 
    None   = use conmfiguration in users home directory ~/.ddb/ddb.conf
    False  = Empty configuration, No configuration loaded or saved
    string =  The specific configuration file to use
 Debug:
  Turn debugging verbosity on

ddb_context.query("Select * from test.mock")

Example:

```
import ddb
import json 


def example1():
    engine=ddb.engine(mode='object')
    # defining the table.
    # not needed if you define out of code in the cli app with "create table"
    # you could even create the table with a query in code, and not use the class function
    # define table is a temporary table definition
    engine.define_table(table_name='test_table',
                        database_name='test_db',
                        field_delimiter=',',
                        columns=['id','first_name','last_name','email','gender','ip_address'],
                        data_file='/home/nd/chris17453/ddb/source/test/MOCK_DATA.csv')



    length=10
    for page in range(1,3):
        print ("Page: {0}".format(page+1))
        # standard query
        query="use test_db; SELECT * FROM test_table ORDER BY email desc LIMIT {0},{1}".format(page*length,length)

        # an array of matched results
        # None if an invalid query or error
        # an empty array if nothing matches the query
        results=engine.query(query)
        #print (json.dumps(results,indent=4) )
        for r in results.data:
            print("ID: {0} Email: {1}".format(r['data']['id'],r['data']['email']))
        print (results.columns)


        # The output should look like this
        '''
        [ddb]$ python examples/example.py 
        Page: 2
        ID: 118 Email: ybeste39@weibo.com 
        ID: 328 Email: ybeelby93@sciencedaily.com
        ID: 232 Email: xwhitmarsh6f@zdnet.com
        ID: 578 Email: xroslingg1@skyrock.com
        ID: 151 Email: wyouel46@mlb.com
        ID: 939 Email: wwoolhouseq2@phoca.cz
        ID: 959 Email: wwinterburnqm@weather.com
        ID: 230 Email: wwilkenson6d@mediafire.com
        ID: 696 Email: wwaistelljb@hhs.gov
        ID: 991 Email: wpettipherri@hc360.com
        Page: 3
        ID: 666 Email: wmcgroryih@wufoo.com
        ID: 228 Email: wlomasney6b@weebly.com
        ID: 445 Email: wjeynesscc@vimeo.com
        ID: 414 Email: wguerrerobh@canalblog.com
        ID: 881 Email: weverog@columbia.edu
        ID: 461 Email: wderyebarrettcs@harvard.edu
        ID: 577 Email: wdaymontg0@quantcast.com
        ID: 487 Email: wcrippelldi@quantcast.com
        ID: 593 Email: wburnsellgg@eepurl.com
        ID: 161 Email: wburbridge4g@xing.com
        [ddb]$ 

        '''

if __name__ == '__main__':
    example1()

# on error data=None
```





