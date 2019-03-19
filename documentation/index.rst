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
DROP
````
UPDATE
``````
@TRUNCATE TABLE
```````````````
Data Manipulation Statements 
----------------------------
SELECT
``````
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
If the system variable is invalid, an error is raised.

Example:
 SET @what=1,OUTPUT_MODULE=TERM;

 Results:
  Success or Failure

SHOW COLUMNS
````````````
SHOW TABLES
```````````
Example:

+----------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
+ database                                                                                           + table                                                                                              +
+====================================================================================================+====================================================================================================+
|main                                                                                                |test                                                                                                |
+----------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+


SHOW VARIABLES
``````````````
Display all system and user variables.

Example:
 SHOW VARIABLES()

Results:
 +-----------------------------+-----------------------------+-----------------------------+
 |type                         |name                         |value                        |
 +=============================+=============================+=============================+
 |system                       |AUTOCOMMIT                   |True                         |
 +-----------------------------+-----------------------------+-----------------------------+
 |system                       |OUTPUT_MODULE                |TERM                         |
 +-----------------------------+-----------------------------+-----------------------------+
 |system                       |OUTPUT_STYLE                 |RST                          |
 +-----------------------------+-----------------------------+-----------------------------+
 |user                         |WHAT                         |1                            |
 +-----------------------------+-----------------------------+-----------------------------+


Utility Statements
------------------
USE 
```
Change the curent database context. The default is main.

Example:
 USE test;

Results:
 Querys executed without a specified database will execute against this database.


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


